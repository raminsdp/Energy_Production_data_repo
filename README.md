# <p align="center">Solar Energy Production</p>

![Solar Panels in Bavaria](https://www.energie-experten.org/fileadmin/_processed_/e/1/csm_Muenchen_80939_PV-Anlage_Allianz_Arena_Foto_01_GOLDBECK_SOLAR_c5bacdeb45.jpg)

## About the Project <a name="about"></a>  

In regards of the transformation of the german and european energy market and the political supported growth of renewable energies, there is still an issue with energy production, as no control on the actual production is possible, but rather depends solely on environmental conditions (day/night, wind/no wind).
This project focuses on a very specific german area and energy production, solar power in the state of Bavaria, with the possibility to upscale it beyond these settings.
A strategical 1-year-forecast as well as daily predictions for operational planning are the desiered goals of this project.

## Table of Contents
1. [About The Project](#about)
2. [Data Gathering, EDA and Preprocessing](#eda)
3. [Modelling](#modelling)
4. [Use Cases](#use-cases)
5. [Outlook](#outlook)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)

## Data Gathering, EDA and Preprocessing <a name="eda"></a> 

### Data Gathering
Public Data was scraped from the following sources:
- [Deutscher Wetterdienst - DWD](https://opendata.dwd.de/)
- [TenneT](https://netztransparenz.tennet.eu/de/strommarkt/transparenz/transparenz-deutschland/netzkennzahlen/)
- [Marktstammdatenregister](https://www.marktstammdatenregister.de/MaStR/Einheit/Einheiten/OeffentlicheEinheitenuebersicht)

The raw dataframe can be re-created using the "data_gathering.py" script, which needs some files to be downloaded before (as commented in the first lines of the script). The already gathered and preprocessed data for 2015 to 2023 can be found in the df_solar_energy_2015_2023.csv file (/Dataset/preprocessed_data/). 
The dataset is a time-series from 01.01.2015 to 31.12.2023 with daily data on actual produced energy (MW per day), weather parameter (sun hours (h) and two types of solar radiation (J/cm²)) and registered solar panels (in units of kilowatt peak (gross/net)).
In total **3287** entries are available in the dataframe.

### Explorative Data Analysis

Plausibility of data was checked, missing values were imputed. Data from Tennet and Marktstammdatenregister are seemingly plausible and have no missing values. Non-linear, positive trends were to be found for produced energy and capacity of solar panels. The 18 columns of 6 DWD Stations have 23 - 1069 missing or implausible data points, which had to be imputed. No trend was observable for weather parameters in this timeframe.

### Preprocessing of given Data

For imputation of missing values the **mean** value of the **median** of the row (actual day and respective physical parameter) and the **median** of the column (respective day over the years) was calculated and used. Since the outcome is acceptable, a different approach with e.g. weighted medians, especially for the station itself (=column) was skipped.<br>
Since daily predicted energy production is a target of this project, the technical capacity for this needs to be expressed as a value within the dataset. Therefore the daily **cumulative** solar panels was calculated, based on registering date at Marktstammdatenregister.  

## Modelling <a name="modelling"></a>
The dataset is a combination of various variables from a 9-year-timeframe. It can either be used for a time-series approach to forecast e.g. a complete period of 1 year (extrapolation) or for predicting a target value with e.g. regression (interpolation).

### Regression

A regression model was used to predict daily produced solar energy with the given features. Several models for regression and artificial neural networks were tested and finally a RandomForestRegressor showed the best fit.

| ![RandomForestRegressor](https://github.com/raminsdp/Energy_Production_data_repo/blob/main/Dataset/images/rf_model_aim.PNG) | ![LSTM Neural Network](https://github.com/raminsdp/Energy_Production_data_repo/blob/main/Dataset/images/lstm_ann.PNG) |
| --- | --- |

### Time-Series Approach

For forecasting of a whole year a SARIMA model was used, since seasonality was confirmed by mandatory data analysis within a time-series approach.

| ![Forecast SARIMA 2023](https://github.com/raminsdp/Energy_Production_data_repo/blob/main/Dataset/images/forecast_sarima_2023.png) | ![ACF and PACF](https://github.com/raminsdp/Energy_Production_data_repo/blob/main/Dataset/images/pacf_acf.png) |
| --- | --- |

## Use Cases <a name="use-cases"></a> 

**Customers** will have the advantage to have the forecasted energy production visualized, to have their minds eased about any worries concerning power supply. For this the 1-year forecast of the time-series approach is applicable.<br>
**Companies** in the field of energy production can look forward with daily predicted power generation, to e.g. plan their production and energy storage of virtual power plants in advance. The regression model is to be used for the prediction.

## Outlook <a name="outlook"></a> 

This project was successfully validated with public data for Bavaria, Germany. Data for weather and solar panels are available for the whole of Germany from the specific sources. The produced solar energy is from the Netzbetreiber TenneT, who also publishes data for wind energy, for its supplied regions of Bayern, Rheinland-Pfalz, Niedersachsen/Bremen and Schleswig-Holstein/Hamburg. Data for other regions may not be available at this scale of transparency.

In a subsequent project additional data can be used fore increased precision. Further scale of this project could be different states, countries and type of renewable energy (wind). Also, a regression-approach for a yearly forecasting using trends and means of given data can be tried and compared to the time-series approach.


## Contributing <a name="contributing"></a> 

The project was realised as part of the StackFuel Portfolio Projekt in March 2024 from following participants:
- Mohammad Hussain Rajai [GitHub](https://github.com/mhrajai) [LinkedIn](https://www.linkedin.com/in/mohammad-hussain-rajai-b6a729197/)
- Ramin Sadrpanah [GitHub](https://github.com/raminsdp) [LinkedIn](https://www.linkedin.com/in/ramin-sadrpanah-32bba8b8)
- Ullrich Seidel [GitHub](https://github.com/ullrich-seidel)

## License <a name="license"></a> 

The used data is from public sources with following license regulations:
- [DWD](https://www.dwd.de/DE/service/copyright/copyright_node.html)
- [TenneT](https://netztransparenz.tennet.eu/de/strommarkt/transparenz/)
- [Marktstammdatenregister](https://www.marktstammdatenregister.de/MaStR/Startseite/Impressum)

## Acknowledgements <a name="acknowledgements"></a> 

The project was realised with Jupyter, using following libaries and frameworks for EDA, modelling and visualisation:

- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
- [Seaborn](https://seaborn.pydata.org/)
- [statsmodels.api](https://www.statsmodels.org/stable/index.html)
- [Scikit Learn](https://scikit-learn.org/)
- [TensorFlow](https://www.tensorflow.org/)

