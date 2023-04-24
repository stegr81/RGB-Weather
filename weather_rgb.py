import requests
from datetime import datetime
from datetime import timedelta
import schedule
#import board, neopixel
class Forecast:
    def __init__(self,api_key = "f9a3c987-15db-40fb-abc6-312e6381e68f", locator_code = "350893"):
        self.__temperature_dict={
            '-5':(0,0,153),
            '-4':(0,0,153),
            '-3':(0,0,255),
            '-2':(0,0,255),
            '-1':(0,128,255),
            '0':(0,128,255),
            '1':(102,178,255),
            '2':(102,178,255),
            '3':(153,204,255),
            '4':(153,204,255),
            '5':(204,229,255),
            '6':(204,229,255),
            '7':(204,255,255),
            '8':(204,255,255),
            '9':(102,255,255),
            '10':(102,255,255),
            '11':(255,255,204),
            '12':(255,255,204),
            '13':(255,255,153),
            '14':(255,255,153),
            '15':(255,255,0),
            '16':(255,255,0),
            '17':(255,178,102),
            '18':(255,178,102),
            '19':(255,128,0),
            '20':(255,128,0),
            '21':(255,255,102),
            '22':(255,255,102),
            '23':(255,0,0,),
            '24':(255,0,0),
            }
        self.__resource = "val/wxfcs/all/json/"
        self.__locator_code = locator_code
        self.__api_key = api_key
        self.__endpoint = f"http://datapoint.metoffice.gov.uk/public/data/{self.__resource}{self.__locator_code}?res=3hourly&key={self.__api_key}"
        self.__list_sites = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=f9a3c987-15db-40fb-abc6-312e6381e68f"
        self.__site_list  = requests.get(self.__list_sites).json()
    
    def get_forecast(self) -> list:
        tomorrow = datetime.today().date()+timedelta(days=1)
        display_date = tomorrow.strftime("%Y-%m-%dZ")
        forecast = requests.get(self.__endpoint).json()
        temperature_list=[]
        if forecast['SiteRep']['DV']['Location']['Period'][1]['value']==display_date:
            for i in forecast['SiteRep']['DV']['Location']['Period'][1]['Rep']:
                temperature_list.append((i['T']))

        temperature_list = self.__pad_temps(temperature_list)
        
        return temperature_list
    
    def __pad_temps(self,temps,val1=0,val2=1,padded_temps=[]) -> list:
        temps = [float(x) for x in temps]
        for x in range(7):
            padded_temps.append((temps[val1]+temps[val2])/2)
            val1+=1
            val2+=1

        for n in range(1,14,2):
            temps.insert(n,padded_temps.pop(0))

        temps = [str(int(x)) for x in temps]
            
        return temps

class Strip():
    def __init__(self):      
        self.__pixel_pin = board.D18
        self.__num_pixels = 15
        self.__order = neopixel.GRB
        self.__pixels = neopixel.NeoPixel(
            self.__pixel_pin, self.__num_pixels, brightness = 0.2, auto_write = False, pixel_order = self.__order
        )

class Weather(Forecast,Strip):
    def __init__(self):
        pass
    
    def get_vals_set_pixels(self):
        self.temps = self.get_forecast()
        for i in self.num_pixels:
            self.__pixels[i] = self.__temperature_dict[self.__temps[i]]
        self.__pixels.show()


weather = Weather()
weather.get_vals_set_pixels()
schedule.every().day.at("23:55").do(weather.set_pixels())

while True:
    schedule.run_pending(weather.self__get_forecast())
    time.sleep(1)
