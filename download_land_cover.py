import http.client

conn = http.client.HTTPSConnection("www.mrlc.gov")
payload = ''
headers = {
  'Accept': 'image/geotiff',
  'Cookie': 'ROUTEID=.2'
}
conn.request("GET", "/geoserver/mrlc_display/NLCD_2016_Land_Cover_L48/wms?service=WMS&request=GetMap&CRS=EPSG:4326&Width=2000&Height=2000&layers=NLCD_2016_Land_Cover_L48&Format=image/geotiff&bbox=-102.9851672619629,34.24527460247113,-87.39462351501466,42.47492527271053&query_layers=NLCD_2016_Land_Cover_L48", payload, headers)
res = conn.getresponse()
data = res.read()
file = open("land_cover.tif", "wb")
file.write(data)
file.close()