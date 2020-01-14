from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import pandas as pd
import numpy as np
# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Flask setup
app = Flask(__name__)


@app.route("/")
def welcome():
    return(
        f"Welcome to the Station API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    ppt_list= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    return jsonify(ppt_list)

@app.route("/api/v1.0/stations")
def stations():
    most_active= session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    return jsonify(most_active)




@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >='2016-08-23'). all()
    return jsonify(tobs)

    

@app.route("/api/v1.0/<start>")
def start_temp(start=None):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
     filter(Measurement.date >= start).filter(Measurement.date <= end).all()
     return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
