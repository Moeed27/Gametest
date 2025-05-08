import random
from flask import Blueprint, Response, render_template, request

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from matplotlib.figure import Figure
import requests
import json
from database.enums import Roles
from database.tables import User, CarbonLog

from matplotlib import pyplot
import base64
from io import BytesIO
from config import db
from database import neso_api

import datetime

import config

education_bp = Blueprint('education', __name__, template_folder='templates')

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class LocationForm(FlaskForm):
    latitude = DecimalField("Latitude (degrees)")
    longitude = DecimalField("Longitude (degrees)")
    submit = SubmitField("Calculate!")

def create_monthly_graph(data_in):
    pyplot.figure(figsize=[15.0,5.0])
    pyplot.bar(months, [data_in["outputs"]["monthly"]["fixed"][i]["E_m"] for i in range(12)])
    pyplot.title("Energy Production by Month")
    pyplot.xlabel("Month")
    pyplot.ylabel("Production (kWh)")
    buf = BytesIO()
    pyplot.savefig(buf, format="png", transparent=True)
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def create_angle_pie(angle, label, title, colour, startangle):
    pyplot.figure()
    pyplot.title(title)
    reverse = False
    if(angle < 0):
        angle = abs(angle)
        reverse = True
        
    pyplot.pie([angle, 360 - angle], labels=[label, ""], colors=[colour, "lightgray"], startangle=startangle, counterclock=reverse, shadow=True)
    buf = BytesIO()
    pyplot.savefig(buf, format="png", transparent=True)
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def create_user_carbon_graph():
    dateToday = datetime.date.today()
    
    dayLabels = []
    our_data = []
    
    average_data = []
    
    for i in range(7):
        date = (dateToday - datetime.timedelta(days=i))
        dayLabels.insert(0,days[date.weekday()])
        our_data.insert(0, CarbonLog.get_global_carbon_total(date - datetime.timedelta(days=1), date)[0])
        
        request = f'https://api.carbonintensity.org.uk/intensity/date/{date.isoformat()}'
        response = requests.get(request)
        _data = response.json()
        intensity = 0.0
        for i in range(48):
            actual = _data['data'][i]["intensity"]["actual"]
            if actual != None:
                intensity += actual
            else:
                _data['data'][i]["intensity"]["forecast"]
        intensity /= 48.0
        average_data.insert(0, intensity)
    
    pyplot.figure()
    pyplot.plot(dayLabels, our_data, label = "our users")
    pyplot.plot(dayLabels, average_data, label="average in the UK")
    pyplot.ylabel("Carbon levels (gCO₂/kWh)")
    pyplot.legend()
    buf = BytesIO()
    pyplot.savefig(buf, format="png", transparent=True)
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    average_percentage = 0.0
    for i in range(7):
        average_percentage += (float(our_data[i]) / float(average_data[i])) * 100.0
    
    average_percentage = round(average_percentage / 7.0)
    
    return data, average_percentage

@education_bp.route("/information")
def information():
    
    global_eco_points = db.session.execute(db.select(db.func.sum(User.ecopoints))).scalar()
    
    data, average_percentage = create_user_carbon_graph()
    
    return render_template("education/information.html", global_eco_points = global_eco_points, graph_data = data, average_percentage = average_percentage)

@education_bp.route("/sunTracker", methods=['GET', 'POST'])
def sunTracker():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if lat == None or lon == None:
        return render_template("education/sunTracker.html", error=False)

    apiRequest = "https://re.jrc.ec.europa.eu/api/PVcalc?lat={}&lon={}&peakpower=1&loss=14&optimalangles=1&fixed=1&outputformat=json".format(lat,lon)

    _data = requests.get(apiRequest)
    
    if _data.ok:
    
        print("\n\n request: " , apiRequest, "\n\n")
        
        print("\n\n data is as follows: \n")
        
        print(_data.text)
        
        dataJson = _data.json()

        ed = dataJson["outputs"]["totals"]["fixed"]["E_d"]
        #NOTE: this number represents "peak" daily power for solar panels, 4kWh
        best_ed = 4.0
        efficiency = int((ed / best_ed) * 100.0)

        best_em = 0.0
        best_month = "None"
        
        for i in range(12):
            em = dataJson["outputs"]["monthly"]["fixed"][i]["E_m"]
            if em > best_em:
                best_em = em
                best_month = months[i]
        
        azimuth = dataJson["inputs"]["mounting_system"]["fixed"]["azimuth"]["value"]
        slope = dataJson["inputs"]["mounting_system"]["fixed"]["slope"]["value"]

        return render_template("education/sunTracker.html", data=dataJson, graph = create_monthly_graph(dataJson), slopePie = create_angle_pie(slope, f"{slope}°", "Optimal slope (vertical) angle", "red", 180),azimuthPie = create_angle_pie(azimuth, f"{azimuth}° North", "Optimal azimuth (horizontal) angle", "blue", 90), efficiency = efficiency, best_month = best_month, best_em = best_em, city="", latitude=lat, longitude=lon, success=True)
    else:
        return render_template("education/sunTracker.html", error=True)