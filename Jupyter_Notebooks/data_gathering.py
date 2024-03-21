# files that needed to be downloaded before running the script:
# data source: https://netztransparenz.tennet.eu/de/strommarkt/transparenz/transparenz-deutschland/netzkennzahlen/tatsaechliche-und-prognostizierte-solarenergieeinspeisung/bayern/
# manually filtered for 2023-01-01 to 2023-12-31, output will be named 'solarEnergyFeedIn_BY_2023-01-01_2023-12-31.csv'
# the file have to be saved in Dataset/raw_data/ (folder has to be created)
#
# data source: http://www.marktstammdatenregister.de/MaStR/Einheit/Einheiten/OeffentlicheEinheitenuebersicht?filter=Inbetriebnahmedatum%20der%20Einheit~lt~%2701.01.2024%27~and~Inbetriebnahmedatum%20der%20Einheit~gt~%2731.12.2014%27~and~Bundesland~eq~%271403%27~and~Energietr%C3%A4ger~eq~%272495%27
# filters for Bavaria, solar energy and targeted timeframe already applied in the link
# 465169 data points in 94 csv files, manually downloaded on March 08, 2024 (daily changes to data occur)
# the files have to be saved in Dataset/raw_data/

import pandas as pd
import os
import datetime as dt
import numpy as np

### weather data
import requests, zipfile
from io import BytesIO
from io import StringIO

# data source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/solar/

# overview of DWD stations
url = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/solar/ST_Tageswerte_Beschreibung_Stationen.txt'

df_dwd = pd.read_fwf(url,encoding = "ISO-8859-1",colspecs=[(0,5),(6,14),(15,23),(36,38),(43,51),(53,60),(61,84),(142,165)])[1:]
df_dwd.columns = ['Stations_id', 'von_datum', 'bis_datum', 'Stationshoehe', 'geoBreite', 'geoLaenge', 'Stationsname', 'Bundesland']
# getting id's for stations in Bavaria and with data within targeted timeframe
mask = (df_dwd.loc[:,'Bundesland'] == 'Bayern') & (df_dwd.loc[:,'von_datum'] < '20150101') & (df_dwd.loc[:,'bis_datum'] >= '20231231')
stations = list(df_dwd.loc[mask,'Stations_id'])

# creating empty Dataframe
df_stations = pd.DataFrame({'date': pd.date_range(start='1/1/2023', freq='1d', periods=365)})

# automated data scraping from web source
for station in stations:
    req = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/solar/tageswerte_ST_'+station+'_row.zip')
    zip = zipfile.ZipFile(BytesIO(req.content))  
    f = zip.open(zip.namelist()[-1])
    content = f.read()
    s=str(content,'utf-8')
    data = StringIO(s) 
    df_stat = pd.read_csv(data,sep=';',parse_dates=['MESS_DATUM'],usecols=    ['MESS_DATUM','FD_STRAHL','FG_STRAHL','SD_STRAHL'])
    mask = (df_stat.loc[:,'MESS_DATUM'] >= '2023-01-01') & (df_stat.loc[:,'MESS_DATUM'] <= '2023-12-31')
    df_stat.columns =['date',station+'_FD_STRAHL',station+'_FG_STRAHL',station+'_SD_STRAHL']
    df_stations = df_stations.merge(df_stat.loc[mask,:],on='date')


### production of solar energy in Bavaria in megawatt
df_en_raw = pd.read_table('../Dataset/raw_data/solarEnergyFeedIn_BY_2023-01-01_2023-12-31.csv',sep=';',parse_dates=['Datum'],decimal=',')

# create empty dataframe based on targeted dates
df_en = pd.DataFrame({'date': pd.date_range(start='1/1/2023', freq='1d', periods=365)})
df_en.loc[:,'Prog_in_MW'] = pd.DataFrame(df_en_raw.groupby(['Datum'], as_index=False)['Prognostiziert in MW'].sum()).iloc[:,1]
df_en.loc[:,'Act_in_MW'] = pd.DataFrame(df_en_raw.groupby(['Datum'], as_index=False)['Tatsaechlich in MW'].sum()).iloc[:,1]


### registered solar modules (MWp)
def read_and_combine_files(start, end, folder_path):
    # list for caching extracted data
    dfs = []

    # going through downloaded files
    for i in range(start, end + 1, 5000):
        # Erstelle den Dateinamen basierend auf dem Nummernbereich
        file_name = f"Stromerzeuger_{i}_bis_{i + 4999}.csv" 

        # create path to file
        file_path = os.path.join(folder_path, file_name)

        # read csv and append it to dataframe
        df = pd.read_csv(file_path, delimiter=';')
        dfs.append(df)

    # read in of last file, name has to be adjusted 
    last_file_path = os.path.join(folder_path, 'Stromerzeuger_465001_bis_465169.csv') # highest number has to be adjusted
    last_df = pd.read_csv(last_file_path, delimiter=';')

    # append data to dataframe
    dfs.append(last_df)

    # Kombiniere alle DataFrames nach dem Index
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    return combined_df

folder_path = r'../Dataset/raw_data/Marktstammdatenregister/'

combined_df = read_and_combine_files(1, 464999, folder_path)

# creating empty Dataframe
df_modules = pd.DataFrame({'date': pd.date_range(start='1/1/2015', end='12/31/2023', freq='1d')})

# masking data with 'Betriebs-Status' 'In Betrieb' (actual in operation)
mask_combined_df = (combined_df['Betriebs-Status'] == 'In Betrieb')
df_combined_filtered = combined_df.loc[mask_combined_df, :].copy()  

# 'Inbetriebnahmedatum der Einheit' converting to datetime
df_combined_filtered['Inbetriebnahmedatum der Einheit'] = pd.to_datetime(df_combined_filtered['Inbetriebnahmedatum der Einheit'], format="%d.%m.%Y", errors='coerce')

# calculating grouped sum of 'Bruttoleistung der Einheit' and 'Nettonennleistung der Einheit' based on 'Inbetriebnahmedatum der Einheit' 
grouped_sum = df_combined_filtered.groupby('Inbetriebnahmedatum der Einheit').agg({
    'Bruttoleistung der Einheit': lambda x: x.str.replace(',', '.').astype(float).sum(),
    'Nettonennleistung der Einheit': lambda x: x.str.replace(',', '.').astype(float).sum()
}).reset_index()

# rename columns
grouped_sum = grouped_sum.rename(columns={'Bruttoleistung der Einheit': 'Bruttoleistung', 'Nettonennleistung der Einheit': 'Nettoleistung'})

# merge grouped sums on date
df_modules = df_modules.merge(grouped_sum, left_on='date', right_on='Inbetriebnahmedatum der Einheit', how='left').fillna(0)

# drop unnecessary column
df_modules = df_modules.drop(columns=['Inbetriebnahmedatum der Einheit'])

## alternatively collecting data from 1 downloaded file: ##
## data source: https://download.marktstammdatenregister.de/Gesamtdatenexport_20240306_23.2.zip (or any current version from 'Gesamtdatenauszug vom Vortag' at https://www.marktstammdatenregister.de/MaStR/Datendownload)
## files: EinheitenSolar_1-39.xml, manually unpacked in /Dataset/raw_data
## script can be applied to any state and/or timeframe, but will take several hours for a run
#
#import xml.etree.ElementTree as ET
#
#files = list(range(1,40)) # manually setting numbers 1-39
# creating empty dataframe
#df_mod_raw = pd.DataFrame(columns=['Datum', 'PLZ', 'Bruttoleistung','Nettonennleistung','Inbetriebnahme'])
#counter = 0
#for file in files:
#    source = 'Dataset/raw_data/EinheitenSolar_'+str(file)+'.xml'
#    tree = ET.parse(source)
#    root = tree.getroot()
#    
#    for einheit in root.findall('EinheitSolar'):
#        try: 
#            land = einheit.find('Bundesland').text
#        except:
#            land = 'Unbekannt'
#        if land == '1403': # Bundesland 1403 = Bayern
#            try: 
#                inbetrieb = einheit.find('Inbetriebnahmedatum').text
#            except:
#                inbetrieb = 'Ausser_Betrieb'
#            
#            if inbetrieb.startswith(('2015','2016','2017','2018','2019','2020','2021','2022','2023')):  
#                plz = einheit.find('Postleitzahl').text 
#                brutto = float(einheit.find('Bruttoleistung').text)
#                netto = float(einheit.find('Nettonennleistung').text)
#                datum = einheit.find('DatumLetzteAktualisierung').text
#        
#                datum = datum[:10]
#                df_mod_raw.loc[counter] = [datum,plz,brutto,netto,inbetrieb]
#                counter = counter + 1

### merging dataframes
df_final_raw_2015_2023 = df_modules.merge(df_modules,df_en, on = 'date')
df_final_raw_2015_2023 = df_final_raw_2015_2023.merge(df_stations, on = 'date')
df_final_raw_2015_2023.to_csv('../Dataset/preprocessed_data/df_final_raw_2015_2023.csv')