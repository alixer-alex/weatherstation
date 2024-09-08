import json
import urllib.parse
import urllib.request
import time
from pathlib import Path



class formatError(Exception):
    pass


class siteNotFound(Exception):
    pass

class numberError(Exception):
    pass

class nominatim_internet:
    def __init__(self, query:str):
        self.url='https://nominatim.openstreetmap.org/search?q='
        #initializes the query, response, longitude, latitude
        self.q=query
        self.response=None
        self.longitude=0
        self.latitude=0
    def communication(self)->None:
        'communicates with the server, downloads the json data'
         #constructs url
        elements=self.q.split(',')
        terms=[]
        #implement error
        for e in elements:
            terms+= e.split()
        for t in terms:
            self.url= self.url+t+'+'
        self.url=self.url[:len(self.url)-1]+'&format=json'
        #opens url
        response=None
        try:
            #accesses the url and the data from the website
            request= urllib.request.Request(self.url,headers={'Referer':'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/azhuang3'})
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding='utf-8')
            #checks for response and type of content
            if not response.getcode()==200:
                raise siteNotFound
            if not response.info().get_content_type()== 'application/json':
                raise formatError
            #gets the first result
            self.response= json.loads(json_text)[0]
            #stops for 1 sec
            time.sleep(1)
            
        #handles errors
        except siteNotFound:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('NOT 200')
        except IndexError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except formatError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except urllib.error.URLError:
            print('FAILED')
            print('NETWORK')
        
    
        finally:
            if response != None:
                response.close()
    
    def interpret(self)->None:
        'interprets the data, gets the longitude and latitude'
        try:
            self.longitude= self.response.get('lon')
            self.latitude= self.response.get('lat')
            if not type(self.longitude)  == str:
                raise numberError
            if not type(self.latitude)== str:
                raise numberError
        except KeyError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except numberError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')

   
            
class nws_internet:
    def __init__(self, latitude:float, longitude:float):
        self.url='https://api.weather.gov/points/'+str(latitude)+','+ str(longitude)
        self.response= None
    def communication(self)->'Geo-JSON':
        'communicates with the internet, gets the url of the nws data twice'
        
        response= None
        new_response=None
        try:
            #handles the first request, for the first link
            request= urllib.request.Request(self.url,headers={'User-Agent': ('https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/azhuang3@uci.edu'), 'Accept': 'application/geo+json'})
            response = urllib.request.urlopen(request)
            #checks for response and type of content
            if not response.getcode()==200:
                raise siteNotFound
            if not response.info().get_content_type()== 'application/geo+json':
                raise formatError
            json_text = response.read().decode(encoding='utf-8')
            self.response= json.loads(json_text)
            
            #tries to get the second link
            new_url=self.response.get('properties').get('forecastHourly')
            new_request=urllib.request.Request(new_url+'/?units=us',headers={'User-Agent': ('https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/azhuang3@uci.edu'), 'Accept': 'application/geo+json'})
            new_response=urllib.request.urlopen(new_request)
            #checks for response and type of content
            if not new_response.getcode()==200:
                raise siteNotFound
            if not new_response.info().get_content_type()== 'application/geo+json':
                raise formatError
            new_json_text=new_response.read().decode(encoding='utf-8')
            self.response=json.loads(new_json_text)
            
            
        except siteNotFound:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('NOT 200')
        except urllib.error.URLError:
            print('FAILED')
            print('NETWORK')
        except KeyError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except formatError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
            
        finally:
            if response != None:
                response.close()
            if new_response != None:
                new_response.close()
    def interpret(self)->None:
        'interprets the data, gets the hourly report'
        try:
            self.response=self.response.get('properties')
            self.response=self.response.get('periods')
            if not type(self.response)== list:
                raise numberError
        except KeyError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except numberError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')





            
class nominatim_file:
    def __init__(self, file:Path):
        self.file=Path(file)
        self.response=None
        self.latitude=0
        self.longitude=0
    def communication(self)->'JSON':
        'communicates with the file, gets the data from the file'
        file=None
        try:
            file=open(self.file,'r')
            #loads the file in a json format
            get_json=json.load(file)
            self.response=(get_json[0])
        except FileNotFoundError:
            print('Failed')
            print(self.file)
            print('MISSING')
        except json.decoder.JSONDecodeError:
            print('Failed')
            print(self.file)
            print('FORMAT')
        finally:
            if file != None:
                file.close()

            
    def interpret(self)->float:
        'gets the info from the files, longitude and latitude'
        try:
            self.longitude= self.response.get('lon')
            self.latitude= self.response.get('lat')
            if not type(self.longitude) == str:
                raise numberError
            if not type(self.latitude)==str:
                raise numberError
        except KeyError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except numberError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except AttributeError:
            print('FAILED')
            print(self.file)
            print('FORMAT')



class nws_file:
    def __init__(self, file:Path):
        self.file=file
        self.response=None
    def communication(self)->None:
        'communicates with the file, loads the hourly report'
        file=None
        try:
            file=open(self.file,'r')
            get_json=json.load(file)
            self.response=get_json
        except FileNotFoundError:
            print('FAILED')
            print(self.file)
            print('MISSING')
        except json.decoder.JSONDecodeError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        finally:
            if file != None:
                file.close()
    def interpret(self)->None:
        'pulls every hour from the files data'
        try:
            self.response=self.response.get('properties')
            self.response=self.response.get('periods')
            if not type(self.response) == list:
                raise numberError
        except KeyError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except numberError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except AttributeError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
            
class reverse_nominatim:
    def __init__(self, latitude:float, longitude:float):
        self.url='https://nominatim.openstreetmap.org/reverse?lat='+str(latitude)+'&lon='+str(longitude)+'&format=json'
        #implement error
        self.response=None
        self.display_name=None
    def communication(self)->None:
        'communicates with the server, gets the data'
        response=None
        #opens url
        try:
            request= urllib.request.Request(self.url,headers={'Referer':'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/azhuang3'})
            response = urllib.request.urlopen(request)
            #checks for response and type of content
            if not response.getcode()==200:
                raise siteNotFound
            if not response.info().get_content_type()== 'application/json':
                raise formatError
            json_text = response.read().decode(encoding='utf-8')
            #gets the first result
            self.response= json.loads(json_text)
            #stops for 1 sec
            time.sleep(1)
        except siteNotFound:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('NOT 200')
        except urllib.error.URLError:
            print('FAILED')
            print('NETWORK')
        except KeyError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        except formatError:
            print('FAILED')
            print(str(response.getcode())+ ' '+self.url)
            print('FORMAT')
        finally:
            if response != None:
                response.close()
            
    
    def interpret(self)->None:
        'interprets the data, gets the display name'
        try:
            self.display_name=self.response.get('display_name')
            if not type(self.display_name)==str:
                raise numberError
        except KeyError:
                print('FAILED')
                print('200 ' + self.url)
                print('FORMAT')
        except numberError:
            print('FAILED')
            print('200 '+self.url)
            print('FORMAT')


class reverse_file:
    def __init__(self, file:Path):
        self.file=file
        self.response=None
        self.display_name=None
    def communication(self)->None:
        'communicates with and opens the file'
        file=None
        try:
            file=open(self.file,'r')
            get_json=json.load(file)
            self.response=get_json
        except FileNotFoundError:
            print('Failed')
            print(self.file)
            print('MISSING')
        except json.decoder.JSONDecodeError:
            print('Failed')
            print(self.file)
            print('FORMAT')
        finally:
            if file != None:
                file.close()
    def interpret(self)->None:
        'interprets the data, gets the display name'
        try:
            self.display_name=self.response.get('display_name')
            if not type(self.display_name)==str:
                raise numberError
        except KeyError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except numberError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
        except AttributeError:
            print('FAILED')
            print(self.file)
            print('FORMAT')
