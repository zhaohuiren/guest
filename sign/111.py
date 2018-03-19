import requests
from addict import Dict
def weater():
    r=requests.get('https://free-api.heweather.com/s6/weather/forecast?location=北京&key=4e6ea60db7634f3ba31616c733500301')
    a = r.json()
    dictionary = Dict(a)
    cond_txt_d = dictionary.HeWeather6[0].daily_forecast[0].cond_txt_d


    weater=cond_txt_d
    print(weater)
weater()