import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date>"   
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert query results to dictionary using date as key and prcp as value"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
    # Query stations
    results = session.query(Station.name, Station.id, Station.station, Station.elevation, Station.latitude, Station.longitude).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    stations = []
    for name, id, station, elevation, latitude, longitute in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["elevation"] = elevation
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitute
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
    recent_12_mo = dt.date(2017,8,23) - dt.timedelta(days = 365)
    # Query dates and temperatures of most active station for last year    
    recent = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
        filter(Measurement.date >= recent_12_mo).\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    recent_tobs = []
    for date, tobs, station in recent:
        recent_dict = {}
        recent_dict["date"] = date
        recent_dict["tobs"] = tobs
        recent_dict["station"] = station
        recent_tobs.append(recent_dict)
    
    return jsonify(recent_tobs)


@app.route("/api/v1.0/<start_date>")
def start(start_date = None):

    session = Session(engine)

    tob_stats_start = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    return jsonify(list(tob_stats_start))

    session.close()

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date = None, end_date = None):

    session = Session(engine)

    tob_stats = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    return jsonify(list(tob_stats))

    session.close()
         
if __name__ == '__main__':
    app.run(debug=True)
