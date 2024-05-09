# sqlalchemy-challenge

## Overview
The analysis utilizes Python, SQLAlchemy, Pandas, and Matplotlib to analyze and visualize climate data stored in a SQLite database. It is divided into two parts: Part 1 involves analyzing and exploring the climate data using Python and Part 2 focuses on designing a Flask API based on the analysis results.

## Part 1: Analyze and Explore the Climate Data
### Connecting to the Database
It begins by connecting to the provided SQLite database (hawaii.sqlite) using SQLAlchemy.

### Precipitation Analysis
- Finds the most recent date in the dataset.
- Queries the previous 12 months of precipitation data.
- Loads the query results into a Pandas DataFrame, sorts it by date, and plots the results as a bar chart.
- Prints summary statistics for the precipitation data.
### Station Analysis
- Calculates the total number of stations in the dataset.
- Finds the most active station and its observation counts.
- Queries the temperature observations `tobs` for the most active station over the previous 12 months.
- Plots the `tobs` data as a histogram.

## Part 2: Design Your Climate App
### Flask API Routes
- /: Home page with a list of available routes.
- /api/v1.0/precipitation: Returns JSON representation of precipitation data for the last 12 months.
- /api/v1.0/stations: Returns JSON list of stations from the dataset.
- /api/v1.0/tobs: Returns JSON list of temperature observations for the previous year from the most active station.
- /api/v1.0/<start>: Returns JSON list of minimum, maximum, and average temperatures from a specified start date.
- /api/v1.0/<start>/<end>: Returns JSON list of temperature statistics for a specified date range.
