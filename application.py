import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL, eprint
from helpers import lookup

import urllib.request, json

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))




@app.route("/search")
def search():
    """Search for places that match query"""

    q = request.args.get("q") + "%"
    return jsonify(db.execute("SELECT * FROM Kaunas WHERE postal_code LIKE :q OR place_name LIKE :q", q=q))

@app.route("/nav")
def nav():
    sandelys = "54.915907,24.00077"
    diffrence = []
    """ All info in one var """
    places = db.execute("SELECT * FROM Kaunas");
    "Getting distance between points "
    print(places)
    start = sandelys
    count = 0
    while count < 5:
        count +=1
        end = places[count]['latitude'] + ',' + places[count]['longtitude']
        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/distancematrix/json?&origins={0}&destinations={1}&key=AIzaSyCZ0M87efEBW6ulVAi9yYZJ_cwS5WQqUC0".format(start,end)) as url:
            data = json.loads(url.read().decode())
            diffrence.append((data['rows'][0]['elements'][0]['distance']['value']))
    return jsonify(data)