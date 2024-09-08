import weatherstation_classes
import weatherstation_math

class noneError(Exception):
    pass


def get_input()-> None:
    'This function gets the users input'
    user_input=input()
    return user_input

def parse_query(query:str, data:dict)->tuple:
    'This function determines the value from the users query'
    seperated_query = query.split()
    #checks if the query is for temperature
    if seperated_query[0] == 'TEMPERATURE':
        
        #air temperature query
        if seperated_query[1]=='AIR':
            
            temp=0
            
            #checks for max or min
            if seperated_query[4]== 'MAX':
                temp=weatherstation_math.temps(data, int(seperated_query[3]), seperated_query[4])
            elif seperated_query[4]=='MIN':
                temp=weatherstation_math.temps(data, int(seperated_query[3]), seperated_query[4])
            #checks for fahrenheit or celsius
            if seperated_query[2] == 'C':
                temp = (weatherstation_math.f_to_c(float(temp[0])),temp[1])
            return temp
            #under periods
        
        #air temperature feels
        elif seperated_query[1]=='FEELS':
            temp=0
            #checks for max or min
            if seperated_query[4]== 'MAX' :
                temp=weatherstation_math.feels_like_temps(data, int(seperated_query[3]), seperated_query[4])
            elif seperated_query[4]=='MIN':
                temp=weatherstation_math.feels_like_temps(data, int(seperated_query[3]), seperated_query[4])
            #checks for fahrenheit or celsius
            if seperated_query[2] == 'C':
                temp = (weatherstation_math.f_to_c(float(temp[0])),temp[1])
            return temp
    #calls humidity function
    elif seperated_query[0] == 'HUMIDITY':
        humidity=weatherstation_math.humidity(data,int(seperated_query[1]),seperated_query[2])
        return humidity
    #calls wind function
    elif seperated_query[0] == 'WIND':
        wind=weatherstation_math.wind(data, int(seperated_query[1]), seperated_query[2])
        return wind
    #calls precipitaion function
    elif seperated_query[0] == 'PRECIPITATION':
        precip=weatherstation_math.precipitation(data,int(seperated_query[1]), seperated_query[2])
        return precip
    elif query=='NO MORE QUERIES':
        raise query_end
        
class query_end(Exception):
    pass

def run():
    #all errors handled elsewhere, stops the program from continuing 
    try:
        #gets the first and second inputs from the user
        first_input=get_input().split()
        second_input=get_input().split()

        #initializes the place data and weather data 
        place_data=None
        weather_data=None

        #initializes whether these three were used, for printing attributes
        nominatim_used=False
        reverse_nominatim_used=False
        nws_used=False
        #parses the first input for nominatim or file
        if first_input[1]=='NOMINATIM':
            location=''
            #constructs the place in case it has spaces in it
            for i in range(2,len(first_input)):
                location+= first_input[i]+' '
            place_data=weatherstation_classes.nominatim_internet(location)
            nominatim_used=True
        
        elif first_input[1]== 'FILE':
            file_path=''
            #constructs the file path in case the file path has a space in it from the .split
            for i in range(2,len(first_input)):
                file_path+= first_input[i]+' '
            place_data= weatherstation_classes.nominatim_file(file_path)
        
        #interprets and communicates with the server   
        place_data.communication()
        place_data.interpret()
        #parses the 2nd input, checks for nws or file
        if second_input[1]=='NWS':
            weather_data=weatherstation_classes.nws_internet(place_data.latitude,place_data.longitude)
            nws_used=True
        elif second_input[1]=='FILE':
            location=''
            for i in range(2,len(second_input)):
                location+= second_input[i]+' '
            weather_data= weatherstation_classes.nws_file(location)
        #interprets this data
        weather_data.communication()
        weather_data.interpret()


        
        final_numbers= []
        final_times=[]
        while True:
            try:
                weather_query=get_input()
                response_and_time=parse_query(weather_query,weather_data.response)
                #puts all the queries into 2 lists, one for numbers and one for times
                if not type(response_and_time)== tuple and not type(response_and_time[0])== str and not type(response_and_time[1])== str:
                    raise noneError
                final_numbers.append(response_and_time[0])
                final_times.append(response_and_time[1])
            except query_end:
                #ends if the user types query end, raised by parse_query
                break
            except noneError:
                if nws_used==True:
                    print('200 ' + weather_data.url)
                    print('FORMAT')
                else:
                    print(weather_data.file)
                    print('FORMAT')
            except TypeError:
                if nws_used==True:
                    print('200 ' + weather_data.url)
                    print('FORMAT')
                else:
                    print(weather_data.file)
                    print('FORMAT')

        #reverse input
        final_input= get_input().split()
        if final_input[1]=='NOMINATIM':
            reverse_data= weatherstation_classes.reverse_nominatim(place_data.latitude, place_data.longitude)
            reverse_nominatim_used=True
        elif final_input[1] == 'FILE':
            file_path=''
            #constructs the input
            for i in range(2,len(final_input)):
                file_path+= final_input[i]+' '
            reverse_data= weatherstation_classes.reverse_file(file_path)
        #communicates and interprets
        reverse_data.communication()
        reverse_data.interpret()


        #prints responses
        if place_data.latitude.startswith('-'):
            place_data.latitude=place_data.latitude[1:]+'/S '
        else:
            place_data.latitude=place_data.latitude+'/N '

        if place_data.longitude.startswith('-'):
            place_data.longitude=place_data.longitude[1:]+'/W '
        else:
            place_data.longitude=place_data.longitude+'/E '
        print('TARGET ' + place_data.latitude+ place_data.longitude)
        print(reverse_data.display_name)
        for x in range(0,len(final_numbers)):
            print(weatherstation_math.get_time(final_times[x])+'Z '+str(final_numbers[x]))

        if nominatim_used:
            print('**Forward geocoding data from OpenStreetMap')
        if reverse_nominatim_used:
            print('**Reverse geocoding data from OpenStreetMap')
        if nws_used:
            print('**Real-time weather data from National Weather Service, United States Department of Commerce')
    except:
        pass

if __name__=='__main__':
    run()
