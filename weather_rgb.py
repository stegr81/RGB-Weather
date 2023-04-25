import requests
from datetime import datetime
from datetime import timedelta
import schedule
import board, neopixel
class Forecast:
    def __init__(self,api_key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", locator_code = "xxxxxx"):
        self._temperature_dict={
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
        self._resource = "val/wxfcs/all/json/"
        self._locator_code = locator_code
        self._api_key = api_key
        self._endpoint = f"http://datapoint.metoffice.gov.uk/public/data/{self._resource}{self._locator_code}?res=3hourly&key={self._api_key}"
        self._list_sites = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=f9a3c987-15db-40fb-abc6-312e6381e68f"
        self._site_list  = requests.get(self._list_sites).json()
    
    def get_forecast(self) -> list:
        tomorrow = datetime.today().date()+timedelta(days=1)
        display_date = tomorrow.strftime("%Y-%m-%dZ")
        forecast = requests.get(self._endpoint).json()
        temperature_list=[]
        if forecast['SiteRep']['DV']['Location']['Period'][1]['value']==display_date:
            for i in forecast['SiteRep']['DV']['Location']['Period'][1]['Rep']:
                temperature_list.append((i['T']))

        temperature_list = self._pad_temps(temperature_list)
        
        return temperature_list
    
    def _pad_temps(self,temps,val1=0,val2=1,padded_temps=[]) -> list:
        temps = [float(x) for x in temps]
        for x in range(7):
            padded_temps.append((temps[val1]+temps[val2])/2)
            val1+=1
            val2+=1

        for n in range(1,14,2):
            temps.insert(n,padded_temps.pop(0))

        temps = [str(int(x)) for x in temps]
            
        return temps

class Strip:
    def __init__(self):
        self._pixel_pin = board.D18
        self._num_pixels = 15
        self._order = neopixel.GRB
        self._pixels = neopixel.NeoPixel(
            self._pixel_pin, self._num_pixels, brightness = 0.2, auto_write = False, pixel_order = self._order
        )

class Weather(Forecast,Strip):
    def __init__(self):
        super().__init__()
        super(Forecast,self).__init__()
    
    def get_vals_set_pixels(self):
        temps = self.get_forecast()
        for i in range(self._num_pixels):
            try:
                self._pixels[i] = self._temperature_dict[temps[i]]
            except KeyError:
                if int(i)>24:
                    self._pixels[i] = self._temperature_dict[temps['24']])
                elif int(i)<-5:
                    self._pixels[i] = self._temperature_dict[temps['-5']])
        self._pixels.show()
        
        return temps

weather = Weather()
weather.get_vals_set_pixels()
schedule.every().day.at("23:55").do(weather.get_vals_set_pixels)

while True:
    schedule.run_pending()
    time.sleep(15)
