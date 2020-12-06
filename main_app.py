# 1. import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# 2. Create sqlite url and database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 3. Create an Flask app, being sure to pass __name__
app = Flask(__name__)


# 4. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        "Welcome to my 'SQL Home' page! <br/>"
        "<br/>"
        f"Available Routes: <br/>"
        "<br/>"
        f"/api/v1.0/precipitation <br/>"
        "<br/>"
        f"/api/v1.0/stations <br/>"
        "<br/>"
        f"/api/v1.0/tobs <br/>"
        "<br/>"
        f"/api/v1.0/start06152017 <br/>"
        "<br/>"
        f"/api/v1.0/start_end <br/>"
    )

# 5. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    rain_results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    rain_info = []

    for date, prcp in rain_results:
        measurement_dict = {}

        measurement_dict["date"]=date
        measurement_dict["prcp"]=prcp
        rain_info.append(measurement_dict)

    print("Server received request for 'Precipitation' page...")
    return jsonify (rain_info)

# 6. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    rain_sites = session.query(Station.station, Station.name, Station.elevation).all()
    session.close()
    list_sites = []

    for station, name, elevation in rain_sites:
        station_list = {}

        station_list["station"]=station
        station_list["name"]=name
        station_list["elevation"]=elevation
        list_sites.append(station_list)
    
    print("Server received request for 'Station' page...")
    return jsonify (list_sites)

# 7. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temperatures = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == "USC00519397").all()
    session.close()
    year_temps = list(np.ravel(temperatures))

    print("Server received request for 'tobs' page...")
    return jsonify (year_temps)

# 8. Define what to do when a user hits the /start route
@app.route("/api/v1.0/start06152017")
def start06152017():
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs), Measurement.date).filter(Measurement.date == '2017-06-15').all()
    avg_temp = session.query(func.avg(Measurement.tobs), Measurement.date).filter(Measurement.date == '2017-06-15').all()
    max_temp = session.query(func.max(Measurement.tobs), Measurement.date).filter(Measurement.date == '2017-06-15').all()
    
    all_dates_min = session.query(func.min(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').all()
    all_dates_avg = session.query(func.avg(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').all()
    all_dates_max = session.query(func.max(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').all()
    
    session.close()

    print("Server received request for 'start06152017' page...")
    return jsonify (min_temp, avg_temp, max_temp, all_dates_min, all_dates_avg, all_dates_max)



# 9. Define what to do when a user hits the /start_end route
@app.route("/api/v1.0/start_end")
def start_end():
    session = Session(engine)
    vacation_min = session.query(func.min(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').filter(Measurement.date <= '2017-06-25').all()
    vacation_avg = session.query(func.avg(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').filter(Measurement.date <= '2017-06-25').all()
    vacation_max = session.query(func.max(Measurement.tobs), Measurement.date).filter(Measurement.date >= '2017-06-15').filter(Measurement.date <= '2017-06-25').all()  
    session.close()

    print("Server received request for 'start_end' page...")
    return jsonify (vacation_min, vacation_avg, vacation_max)



if __name__ == "__main__":
    app.run(debug=True)