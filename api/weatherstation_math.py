import math
from datetime import datetime
from datetime import timezone

class numberError(Exception):
    pass

def f_to_c(f:float)-> float:
    'converts fahrenheit to celsius'
    return ((f-32)*5 )/9
def c_to_f(c:float)->float:
    'converts celsius to fahrenheit'
    return ((c*9)/5 )+32
def feels_like_temp(t:float, h:int, w:float):
    'gets the feels like temperature'
    if t >= 68.0:
        return -42.379+ (2.04901523*t)+ (10.14333127*h) + (-0.22475541* t*h) + (-0.00683783*(t**2))+ (-0.05481717*(h**2))+(0.00122874*(t**2)*h)+(0.00085282*t*(h**2))+ (-0.00000199*(t**2)*(h**2))
    elif t<= 50.0 and w>3:
        return 35.74+ (0.6215*t) + (-35.75*(w**0.16))+ (0.4275*t*(w**0.16))
    else:
        return t
def temps(data:list, minmaxrange:int, maxormin:str)->int:
    'gets the max or min temperature from a list'
    try:
        #iterates through temps, gets largest one
        temp=data[0].get('temperature')
        time= data[0].get('startTime')
        for x in range(0,minmaxrange):
            if not type(temp)== int or not type(time)==str:
                raise numberError
            current_hour= data[x]
            current_temp= current_hour.get('temperature')
            if maxormin=='MAX':
                if current_temp > temp:
                    temp= current_temp
                    time= data[x].get('startTime')
            else:
                if current_temp<temp:
                    temp=current_temp
                    time= data[x].get('startTime')
        
        #gets 4 decimal places
        return (str(f'{temp:.4f}'), time)
    except KeyError:
        print('FAILED')


    except numberError:
        print('FAILED')


def feels_like_temps(data:list, minmaxrange:int, maxormin:str)->'float,int':
    'gets the max or min feels like temperature from a list of data'
    try:
        #iterates through wind, gets largest one
        first_wind_speed=data[0].get('windSpeed').split()
        temp=feels_like_temp(data[0].get('temperature'),data[0].get('relativeHumidity').get('value'),float(first_wind_speed[0]))
        time = data[0]. get('startTime')
        for x in range(0,minmaxrange):
            if not type(temp)== int or not type(time)==str:
                raise numberError
            current_hour= data[x]
            current_temp= current_hour.get('temperature')
            current_humidity= data[x].get('relativeHumidity').get('value')
            current_windspeed=data[x].get('windSpeed').split()
            feels_like=feels_like_temp(current_temp, current_humidity, float(current_windspeed[0]))
            if maxormin=='MAX':
                if feels_like > temp:
                    temp= feels_like
                    time=data[x].get('startTime')
            else:
                if feels_like < temp:
                    temp= feels_like
                    time=data[x].get('startTime')
        #gets 4 decimal places
        
        return (str(f'{temp:.4f}'), time)
    except KeyError:
        print('FAILED')

    except numberError:
        print('FAILED')
    except TypeError:
        print('FAILED')
        

def humidity(data:list, minmaxrange:int, maxormin:str)-> 'int,float':
    'gets the max or min humidity data from a list'
    try:
        #iterates through humidity, gets largest one
        first_humidity=data[0].get('relativeHumidity').get('value')
        time = data[0]. get('startTime')
        if not type(first_humidity)== int or not type(time)==str:
            raise numberError  
        for x in range(0,minmaxrange):
            current_hour= data[x]
            current_humidity=current_hour.get('relativeHumidity').get('value')
            if not type(current_humidity)== int or not type(time)==str:
                raise numberError 
            if maxormin=='MAX':
                if first_humidity<current_humidity:
                    first_humidity=current_humidity
                    time=data[x].get('startTime')
            else:
                if first_humidity>current_humidity:
                    first_humidity=current_humidity
                    time=data[x].get('startTime')
        #gets 4 decimal places
                  
        return (str(f'{first_humidity:.4f}')+'%',time)
    except KeyError:
        print('FAILED')

    except numberError:
        print('FAILED')


def wind(data:list, minmaxrange:int, maxormin:str)->'int,float':
    'gets the max or min wind data from a list'
    try:
        #iterates through wind, gets largest one
        first_wind_string=data[0].get('windSpeed').split()
        wind=float(first_wind_string[0])
        time = data[0]. get('startTime')
        for x in range (0, minmaxrange):
            if not type(wind)== float or not type(time)==str:
                raise numberError 
            wind_string=data[x].get('windSpeed').split()
            #notated as 10 MPH so getting rid of MPH
            current_wind=float(wind_string[0])
            if maxormin=='MAX':
                if wind<current_wind:
                    wind=current_wind
                    time=data[x].get('startTime')
            else:
                if wind>current_wind:
                    wind=current_wind
                    time=data[x].get('startTime')
         
        return (str(f'{wind:.4f}')+'%',time)
    except KeyError:
        print('FAILED')

    except numberError:
        print('FAILED')
    except TypeError:
        print('FAILED')

def precipitation(data:list, minmaxrange:int, maxormin:str)->'int,float':
    'gets the max or min precipitation data from a list'
    try:
        #iterates through precipitation, gets largest one
        precip=data[0].get('probabilityOfPrecipitation').get('value')
        time = data[0]. get('startTime')
        for x in range(0,minmaxrange):
            if not type(precip)== int or not type(time)==str:
                raise numberError
            current_precip=data[x].get('probabilityOfPrecipitation').get('value')
            if maxormin=='MAX':
                if precip<current_precip:
                    precip=current_precip
                    time=data[x].get('startTime')
            else:
                if precip>current_precip:
                    precip=current_precip
                    time=data[x].get('startTime')
                      
        #gets 4 decimal places
        return (str(f'{precip:.4f}')+'%', time)
    except KeyError:
        print('FAILED')

    except numberError:
        print('FAILED')

def get_time(time:str):
    timestamp= datetime.fromisoformat(time)
    utc= timestamp.astimezone(timezone.utc)
    return utc.isoformat()
