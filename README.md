# sqlalchemy-challenge
This is homework for the University of Minnesota's Data Analytics and Visualization bootcamp using SLWAlchemy and Python. 

## Methodology for climate analysis and data exploration
Connect SQLAlchemy using 'create_engine'
Use 'automap_base()' to reflect tables into classes and save a refrence called 'Station' and 'Measurement'
Link Python to the database by creating a SQLAlchemy session. Close out session at the end of the notebook.

### Precipitation Analysis

Found most recent date in the data set and from there retrieved the last 12 months of precipitation data by querying the 12 preceding months of data. 

Loaded the query results into a Pandas DataFrame and set the index to the date column, sorted by 'date' and plotted using the 'plot' method. 

Used Pandas to print the summary statistics for the precipitation data.

### Station Analysis

Found the station that logged the most readings. Retrieved the last 12 months of readings by querying the 12 preceding months of data.

Loaded query resutls into a Pandas DataFrame and set the index to the date column, sorted by 'date' and generated a histogram of the temperature results.

Designed a query to calculate the total number of stations in the dataset to find the most active station. 

## Step 2 - Climate App

Designed a Flask API based on the queries for precipitation and station analysis. 

