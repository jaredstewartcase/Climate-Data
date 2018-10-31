import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
# The below code allows a new thread to be used. Without this there is an error involving multiple threads
#################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hawaii.sqlite"
db = SQLAlchemy(app)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""

    return (
        f"Available Routes:<br/>"
        f"THIS LINK WILL GIVE THE PRECIPITATION FOR ALL THE DATES<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"THIS LINK WILL GIVE THE ALL THE STATION NAMES<br/>"
        f"/api/v1.0/station<br/>"
        f"THIS LINK WILL GIVE ALL THE TEMPERATURE OBSERVATIONS WITHIN THE LAST YEAR OF DATES<br/>"
        f"/api/v1.0/tobs<br/>"
        f"INPUT THE START DATE IN THE FOLLOWING FORMAT YYYY-MM-DD<br/>"
        f"/api/v1.0/start<br>" 
        f"INPUT THE RANGE OF DATES IN THE FOLLOWING FOMRAT YYYY-MM-DD,YYYY-MM-DD<br/>"
        f"/api/v1.0/start,end"
    )

@app.route("/api/v1.0/precipitation")
def precip():

    """Return a list of all precipitation and corresponding dates"""

# Query all precipitation and dates from measurement database
    prcp_b_ydate = db.session.query(Measurement.date, Measurement.prcp).all()

# Create a dictionary from the row data and append to a list of prcp_date_pairs    
    prcp_date_pairs=[]

    for result in prcp_b_ydate:
        precip_date_dict={}
        precip_date_dict["Date"] = result.date
        precip_date_dict["Precipitation"] = result.prcp
        prcp_date_pairs.append(precip_date_dict)

    return jsonify(prcp_date_pairs)

@app.route("/api/v1.0/station")
def stations():

    """Return a list of all stations from the Station Database"""

# Query all stations from station database
    results = db.session.query(Station.station).all()  

# Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tob():

    """Return a list of temperature and dates from the previous year form the Measurements Database"""

# Query all temp from measurement database
    results = db.session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-23").all()  

# Convert list of tuples into normal list
    tobs_last_year = list(np.ravel(results))

    return jsonify(tobs_last_year)

@app.route("/api/v1.0/<start_date>")
def startdateonly(start_date):

    """Return a list of min, max, and avg temperature from Measurement Database after given start date to last date in database. No end date provided"""

# Query all min, avg, max tobs based on start date
    results = db.session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

# Convert list of tuples into normal list
    start_date_only = list(np.ravel(results))
    
    return jsonify(start_date_only)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_and_end_date(start_date, end_date):

    """Return a list of min, max, and avg temperature from Measurement Database after given start date to last date in database. End date is provided"""

# Query all min, avg, max tobs based on start date and end date
    results = db.session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# Convert list of tuples into normal list
    start_and_end_date_only = list(np.ravel(results))
    
    return jsonify(start_and_end_date_only)

if __name__ == '__main__':
    app.run(debug=True)

