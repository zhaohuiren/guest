from aip import AipOcr
import re

APP_ID='10187073'
API_KEY='Ly28a0F0yBC1itVhN09Q816e'
SECRET_KEY='LYXzLPYLOf4wC3lrTQCnGBGDNGWkQudq'
def get_fille_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()

def data_take(data):
    result=""
    if isinstance(data,list):
        if data:
           for i in data:
               result+=data_take(i)
        else:
            return result

    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):

                result += data_take(value)
            elif isinstance(value, (str)):
                if key.find('words') != -1:
                    result += value + "\n"
    return result



aipOcr=AipOcr(APP_ID,API_KEY,SECRET_KEY)

result1=aipOcr.receipt(get_fille_content("E:\\test.jpg"))

data=data_take(result1)

date_start=data.find("开票日期")+5
date_end=date_start+11
date=data[date_start:date_end]
print(date)