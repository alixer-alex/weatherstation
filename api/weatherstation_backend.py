from flask import Flask, request
import time
from weatherstation_classes import nominatim_internet, nws_internet
from project3 import parse_query
app = Flask(__name__, static_folder='./build', static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/weather')
def get_Weather_data():
    location= request.args.get("location")
    if location:
        print(location)
        time.sleep(1)
        location= nominatim_internet(location)
        location.communication()
        location.interpret()
        tempf,temp2,tempc,tempc2 = get_weather(location.longitude,location.latitude)

        for i in range(4):
            if(i==0):
                temp=tempf
            elif (i==1):
                temp=temp2
            elif(i==2):
                temp=tempc
            elif(i==3):
                temp=tempc2
            while(True):
                if(temp[len(temp)-1]!="0" and temp[len(temp)-1]!="."):
                    break
                elif(temp[len(temp)-1]=="." ):
                    temp=temp[:len(temp)-1]
                    break
                else:
                    temp=temp[:len(temp)-1]
            if(i==0):
                tempf=temp
            elif (i==1):
                temp2=temp
            elif(i==2):
                tempc=temp
            elif(i==3):
                tempc2=temp

     
        print(temp2, tempc, tempc2)
        return{'temp': temp, 'tempmin':temp2 , 'tempc' : tempc , 'tempcmin':tempc2 }, 200

def get_weather(long,lat):
    time.sleep(1)
    instance=nws_internet(lat, long)
    instance.communication()
    instance.interpret()
    query="TEMPERATURE AIR F 24 MAX"
    query2 = "TEMPERATURE AIR F 24 MIN"
    queryc="TEMPERATURE AIR C 24 MAX"
    queryc2="TEMPERATURE AIR C 24 MIN"
    instance=parse_query(query, instance.response)
    instance2=parse_query(query2, instance.response)
    instancec=parse_query(queryc, instance.response)
    instancec2=parse_query(queryc2, instance.response)
    return instance[0], instance2[0], instancec[0], instancec2[0]