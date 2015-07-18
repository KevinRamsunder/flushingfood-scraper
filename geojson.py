import time
import mysql.connector
from string import Template
from geopy.geocoders import Nominatim

geojson = Template('''
{
  "type": "Feature",

  "geometry": {
    "type": "Point",
    "coordinates": [$lat, $long]
  },

  "properties": {
    "title": "$title",
    "description": "$desc",
    "marker-color": "#f86767",
    "marker-size": "small",
    "marker-symbol": "restaurant"
  }
},\n''')

geoquery = Template('SELECT latitude, longitude FROM geodata WHERE phone = \'$num\'')

cnx = mysql.connector.connect(user='root', 
                              password='root',
                              host='127.0.0.1',
                              database='flushingfood')

cursor = cnx.cursor()
query = 'SELECT * FROM restaurants'
cursor.execute(query)
rows = cursor.fetchall()

geostring = ''
cursor2 = cnx.cursor()
for content in rows:
    query2 = geoquery.substitute(num=content[1])
    cursor2.execute(query2)
    rows2 = cursor2.fetchone()

    title = content[0]
    description = 'Cuisine: ' + content[6] + '<br>' + content[2] + ', ' + content[3] + ' ' + content[5] + ' ' + content[4] 
    latitude = rows2[1]
    longitude = rows2[0]

    geostring += geojson.substitute(lat=latitude, long=longitude, title=title, desc=description)

geostring = geostring[:-2]
print('[',geostring,']')

cursor.close()
cursor2.close()
cnx.close()
