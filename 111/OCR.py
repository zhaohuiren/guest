from aip import AipOcr
APP_ID="10187073"
API_KEY='Ly28a0F0yBC1itVhN09Q816e'
SECRET_KEY='LYXzLPYLOf4wC3lrTQCnGBGDNGWkQudq'
aipOcr=AipOcr(APP_ID,API_KEY,SECRET_KEY)
def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()

result=aipOcr.receipt(get_file_content("e:/test.jpg"))
print(result)


