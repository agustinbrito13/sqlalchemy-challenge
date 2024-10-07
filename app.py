# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


MAX_DATE = dt.date(dt.MAXYEAR, 12, 31)
#################################################
# Database Setup
#################################################


# Create engine using the `hawaii.sqlite` database file
engine= create_engine('sqlite:///Resources/hawaii.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with = engine)


# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available routes"""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tstats/&lt;start_date&gt;<br/>"
        f"/api/v1.0/tstats/&lt;start_date&gt;/&lt;end_date&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    with Session(engine) as session:
        # query all precipitations
        results_pcrp = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the query results
    all_prcp = {date: prcp for date, prcp in results_pcrp}

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    with Session(engine) as session:
        # query all stations
        results_stations = session.query(Station.station).all()

    # Create a list from the query results
    all_stations = list(np.ravel(results_stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    with Session(engine) as session:
        # query the last 12 months of temperature observations
        results_tobs = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= '2016-08-23').all()

    # Create a list from the query results
    all_tobs = list(np.ravel(results_tobs))

    return jsonify(all_tobs)
@app.route("/api/v1.0/tstats/<start_date>")
@app.route("/api/v1.0/tstats/<start_date>/<end_date>")
def tstats(start_date, end_date=MAX_DATE):
    """Return the minimum, average, and maximum temperatures for a given start and end date."""

    session= Session(engine)
    # query the min, avg, and max temperatures for the given start and end date
    results_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the query results
    temp_stats = {
        "min_temp": results_temp[0][0],
        "avg_temp": results_temp[0][1],
        "max_temp": results_temp[0][2]
    }

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True, port=5001)


