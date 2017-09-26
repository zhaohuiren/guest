from aip import AipOcr
import json


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

result1=aipOcr.receipt(get_fille_content("D:\\test.jpg"))

data=data_take(result1)
print(data)
