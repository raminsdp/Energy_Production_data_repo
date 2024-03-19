# Solar Energy production

## Table of Contents
1. [About The Project](#about)
2. [Data Gathering, EDA and Preprocessing](#eda)
3. [Modelling](#modelling)
4. [Use Cases](#use-cases)
5. [Outlook](#outlook)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](acknowledgements)


## About the Project <a name="about"></a>  

In regards of the transformation of the german and european energy market and the political supported growth of renewable energies, a strategical forecast and daily prediction will help customers and companies. 
This project focuses on a very specific german area and energy production, solar power in the state of Bavaria, with the possibility to upscale it beyond these settings.
A strategical 1-year-forecast as well as daily predictions for operational planning are the desiered goals of this project.

## Data Gathering, EDA and Preprocessing <a name="eda"></a> 

### Data Gathering
Public Data was scraped from the following sources:
- [DWD](https://www.dwd.de)
- [TenneT](https://www.dwd.de)
- [Marktstammdatenregister](https://www.dwd.de)

The dataframe can be re-created using the "data_gathering.py" script, which needs some files to be downloaded before (as commented in the first lines).The already gathered data for 2015 to 2023 can be found in the df_solar_energy_2015_2023.csv file (/Dataset/preprocessed_data/). 
The dataset is a time-series from 01.01.2015 to 31.12.2023 with daily data on actual produced energy, weather parameter (sun hours and solar radiation) and registered solar panels (in units of kilowatt peak).

### Explorative Data Analysis

Plausibility of data was checked, missing values were imputed. Data from Tennet and Marktstammdatenregister are seemingly plausible and have no missing values.

### Preprocessing of given Data

Since daily predicted energy production is a target of this project, the technical capacity for this needs to be expressed as a value within the dataset. Therefore the daily **cumulative** solar panels was calculated, based on registering date at Marktstammdatenregister.  

## Modelling <a name="modelling"></a>
The dataset is a combination of various variables from a 9-year-timeframe. It can either be used for a time-series approach to forecast e.g. a complete period of 1 year (extrapolation) or for predicting a target value with e.g. regression (intrapolation).

### Time-Series Approach

A SARIMA model was used, since seasonality was confirmed by mandatory data analysis within a time-series approach.

### Regression

Several models were tested and finally a RandomForestRegressor showed the best fit.

## Use Cases <a name="use-cases"></a> 

**Customers** will have the advantage to have the forecasted energy production visualized, to have their minds eased about any worries concerning power supply. 
**Companies** in the field of energy production can look forward with daily predicted power generation, to e.g. plan their production and energy storage of virtual power plants in advance.

## Outlook <a name="outlook"></a> 

This project was successfully validated with public data for Bavaria, Germany. Data for weather and solar panels are available for the whole of Germany from the specific sources. The produced solar energy is from the Netzbetreiber TenneT, who also publishes data for wind energy, for its supplied regions of Bayern, Rheinland-Pfalz, Niedersachsen/Bremen and Schleswig-Holstein/Hamburg. Data for other regions may not be available at this scale of transparency.

## Contributing <a name="contributing"></a> 

The project was realised as part of the StackFuel Portfolio Projekt in March 2024 from following participants:
- [Mohammad](mailto:mh@mail.com)
- [Ramin](mailto:ramin@mail.com)
- [Ullrich](mailto:ulli@mail.com)

## License <a name="license"></a> 

The used data is from public sources with following license regulations:
- DWD
- TenneT
- Marktstammdatenregistedr

## Acknowledgements <a name="acknowledgements"></a> 

The project was realised with Jupyter, using following libaries and frameworks for EDA, modelling and visualisation:

[Pandas](https://pandas.pydata.org/)
Numpy
Matplotlib
Seaborn
SARIMA
Scikit Learn
