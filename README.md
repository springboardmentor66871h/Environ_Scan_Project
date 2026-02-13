Environ Scan Project – Week 1


APIs Used :

1.Open-Meteo Air Quality API (PM2.5, PM10, NO₂, CO, SO₂, O₃)

2.Open-Meteo Weather API (Temperature, Humidity, Wind Speed, Wind Direction)

3.OpenStreetMap (Distance to road, industry, dump site, farmland)


Cities :

Delhi, Mumbai, Hyderabad, Chennai, Bengaluru, Kolkata, Pune, Ahmedabad, Jaipur, Lucknow


Time Range:

Last 90 days 

Final dataset: 21,840 rows × 18 columns


Process :

1.Collected pollution and weather data

2.Extracted location-based features

3.Standardized and cleaned data

4.Pivoted pollution data (long → wide)

5.Merged all datasets

6.Removed duplicates and handled missing values

7.Saved final file: combined_dataset.csv




Project Folder Structure:

   Environ_Scan_Project

           data folder

               raw

                  1. pollution.csv

                  2. weather.csv

                  3. location_features.csv

              processed

                  1. final_combined_dataset.csv



README.md
