# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Create engine to connect to SQLite database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home:API</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            h1 {
                color: #333;
                margin-bottom: 30px;
            }
            nav {
                margin-bottom: 20px;
            }
            nav ul {
                list-style-type: none;
                padding: 0;
                margin: 0;
            }
            nav li {
                display: inline;
                margin-right: 10px;
            }
            nav a {
                text-decoration: none;
                color: #007bff;
            }
            nav a:hover {
                text-decoration: underline;
            }
            .container {
                max-width: 800px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand" href="/">Home</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/api/v1.0/precipitation">Precipitation</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api/v1.0/stations">Stations</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api/v1.0/tobs">Temperature</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api/v1.0/<start>">Start</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api/v1.0/<start>/<end>">Date Range</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container">
            <h1>Welcome to the API Home Page</h1>
            <p> Welcome to my API website! If you decided to treat yourself to a long holiday vacation in Honolulu, Hawaii,<br/> 
            you are on the right place. To help with your trip planning, here, you can explore a variety of weather-related <br/> 
            data and analyses about the area. We've gathered information from different sources to provide you with <br/> 
            valuable insights into weather patterns and trends. </p>
        </div>
        <div class="container">
            <h2>Available Routes:</h2>
            <p> This platform offers several routes for accessing data:</p>
            <ul>
                <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a> - Get precipitation data</li>
                <li><a href="/api/v1.0/stations">/api/v1.0/stations</a> - Get station data</li>
                <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a> - Get temperature observations</li>
                <li><a href="/api/v1.0/&lt;start&gt;">/api/v1.0/&lt;start&gt;</a> - Get min, max, and avg temperatures from a start date</li>
                <li><a href="/api/v1.0/&lt;start&gt;/&lt;end&gt;">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a> - Get min, max, and avg temperatures for a date range</li>
            </ul>
            <p> Feel free to explore and discover more about the Honolulu, Hawaii </p>
        </div>
    </body>
    </html>
    """
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months."""
    # Calculate the date 1 year ago from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365.25)
    
    # Query the last 12 months of precipitation data
    date_precp_query = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in date_precp_query}
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations(): 
    """Return a list of stations."""
    # Query all stations
    results = session.query(Station.station).all()
    
    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the last 12 months."""
    # Get the most active station
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Calculate the date 1 year ago from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365.25)
    
    # Query the last 12 months of temperature observation data for the most active station
    temp_observations = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.station == most_active_station).\
                        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a list
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in temp_observations]
    # tobs_data = [{date: tobs for date, tobs in results}]
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return the minimum, average, and maximum temperatures for a given start date."""
    # Query temperature data for dates greater than or equal to the start date
    temp_observations = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    
    # Convert the query results to a list
    temp_data = {
        "TMIN": temp_observations[0][0],
        "TMAX": temp_observations[0][1],
        "TAVG": temp_observations[0][2]
    }
    temp_data = list(np.ravel(temp_data))
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return the minimum, average, and maximum temperatures for a given start-end range."""
    # Query temperature data for dates within the start-end range
    temp_observations = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    
    # Convert the query results to a list
    temp_data = {
        "TMIN": temp_observations[0][0],
        "TMAX": temp_observations[0][1],
        "TAVG": temp_observations[0][2]
    }
    temp_data = list(np.ravel(temp_data))
    
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)