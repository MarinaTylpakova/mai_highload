import os
import requests
import json
import datetime

from flask import Flask
from flask import request

app = Flask(__name__)


key= ""
def form_url_string(t_request):
    global key
    apikey = "&key=" + key
    url = "https://api.weatherbit.io/v2.0/" + t_request + apikey
    return url

@app.route("/v1/current/")
def current():
    city = request.args.get('city')
    cur_temp = current_temp(city)
    return json.dumps(cur_temp)

@app.route("/v1/forecast/")
def forecast():
    city = request.args.get('city')
    dt = request.args.get('dt')
    cur_temp = current_temp(city, dt)
    return json.dumps(cur_temp)

def current_temp(city: str, dt = None):
    temp = {
        'city': '',
        'unit': 'celsius',
        'temperature': None
    }

    if dt:
        t_request="forecast/daily?city={},RU".format(city)
        
    else:
        t_request = "current?city={},RU".format(city)
    d = 0
 
    f_url = form_url_string(t_request)
    try:
        res = requests.get(f_url)
        data = res.json()
        temp['city'] = city

        if dt:
            for i in range(16):
                if (str(data["data"][i]["datetime"]) == dt):
                    d = i
                    break
            temp['temperature'] = data['data'][d]['temp']
        else:
            temp['temperature'] = data['data'][0]['temp']

    except Exception as e:
        print("Exception (weather):", e)
        pass

    return temp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('LISTEN_PORT', 5000)), debug=True)
