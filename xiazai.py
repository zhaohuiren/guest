import urllib.request

url = 'http://image.bitautoimg.com/bt/car/default/images/logo/masterbrand/png/55/m_9_55.png'
web = urllib.request.urlopen(url)
data = web.read()
#f = open('f:/b.png',"wb")
print(1222)
c='sdf'
b='f:/'+c+'.png'
print(b)
f = open(b,"wb")
f.write(data)
f.close()

