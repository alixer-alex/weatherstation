from flask import Flask, request
import time
from weatherstation_classes import nominatim_internet, nws_internet
from project3 import parse_query
app = Flask(__name__)


@app.route('/api/weather')
def get_Weather_data():
    location= request.args.get("location")
    if location:
        print(location)
        time.sleep(1)
        location= nominatim_internet(location)
        location.communication()
        location.interpret()
        temp = get_weather(location.longitude,location.latitude)
        
        while(True):
            if(temp[len(temp)-1]!="0" and temp[len(temp)-1]!="."):
                break
            elif(temp[len(temp)-1]=="." ):
                temp=temp[:len(temp)-1]
                break
            else:
                temp=temp[:len(temp)-1]
        print(temp)
        return{'temp': temp }, 200

def get_weather(long,lat):
    time.sleep(1)
    instance=nws_internet(lat, long)
    instance.communication()
    instance.interpret()
    query="TEMPERATURE AIR F 24 MAX"
    instance=parse_query(query, instance.response)
    
    return instance[0]