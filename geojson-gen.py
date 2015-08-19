# Generate geojson file from MySQL database.
#
# Executing program: 
#
# Windows:
#
# python geojson-generator.py > [filename].geojson
# 
# The generated geojson file will be outputted to the specified filename.

import re
import time
import mysql.connector
from string import Template

# connect to db
cnx = mysql.connector.connect(user='root', 
                              password='root',
                              host='127.0.0.1',
                              database='flushingfood')

# geojson marker template
template = Template('''
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [$LAT, $LONG]
  },
  "properties": {
    "title": "$TITLE",
    "description": "$DESC",
    "marker-color": "$COLOR",
    "marker-size": "small",
    "marker-symbol": "restaurant"
  },
  "ffm-properties": {
    "title": "$YELP_TITLE",
    "key": "$YELP_KEY"
  }
},\n''')

# tempate for HTML elements
titleTemplate = Template('<a href=\'http://www.yelp.com/biz/$YELP_KEY\' target=\'_blank\'>$NAME</a>')
imgTemplate = Template('<a href=\'http://www.yelp.com/biz/$YELP_KEY\' target=\'_blank\'><img src=\'$RATING_URL\' alt=\'Yelp rating\' style=\'margin-top:5px\'>$REVIEW_COUNT</a>')

# execute SQL query and fetch results
query = '''
SELECT * FROM `restaurants`, `yelp`, `geodata`
WHERE `restaurants`.`phone` = `yelp`.`phone`AND `restaurants`.`phone` = `geodata`.`phone` 
GROUP BY `restaurants`.`phone`'''
cursor = cnx.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
cnx.close()

geostring = ''

# loop through results and generate geodata
for content in rows:
    # database columns
    name = content[0]
    phone = content[1]
    street = content[2]
    city = content[3]
    zipcode = content[4]
    state = content[5]
    cuisine = content[6]
    yelpkey = content[7]
    # phone = content[8]
    # lastUpdated = content[9]
    # yelpkey = content[10]
    ratingURL = content[11]
    ratingCount = content[12]
    # phone = content[13]
    latitude = content[15]
    longitude = content[14]

    # generate title
    title = titleTemplate.substitute(YELP_KEY = yelpkey, NAME = name)
    address = street + ', ' + city + ' ' + state + ' ' + zipcode
    
    # generate rating image url
    if ratingURL == 'NULL':
        description = 'Cuisine: ' + cuisine + '<br>' + address
    else:
        count = ("     " + str(ratingCount) + ' Reviews');
        rating = imgTemplate.substitute(YELP_KEY = yelpkey, RATING_URL = ratingURL, REVIEW_COUNT = count)
        description = rating + '<br>Cuisine: ' + cuisine + '<br>' + address
    

    #if zipcode == '11355':
    #  color = '#3ca0d3'
    #elif zipcode == '11354':
    #  color = '#f86767'
    #elif zipcode == '11358':
    #  color = '#4db634'
    #elif zipcode == '11367' or zipcode == '11366':
    #  color = '#9c89cc'
    #else:
    #  color = '#677da7'
    color = '#3ca0d3';
    if cuisine == 'Chinese':
        color = '#3ca0d3'
    elif cuisine == 'Korean':
        color = '#f86767'
    else:
        color = '#3b9147'

    geostring += template.substitute(LAT= latitude, LONG = longitude, TITLE = title, 
                                     DESC = description, COLOR = color, YELP_TITLE = name, 
                                     YELP_KEY = yelpkey)

# strip extra ending comma
geostring = geostring[:-2]

# print all geodata
print('[', geostring, ']')