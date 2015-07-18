import time
import mysql.connector
import geocoder

# connect to db
cnx = mysql.connector.connect(user='root', 
                              password='root',
                              host='127.0.0.1',
                              database='flushingfood')

# select all rows and execute SQL
query = 'SELECT * FROM `restaurants`'
#query = 'SELECT * FROM `restaurants` WHERE `phone` IN (SELECT `phone` FROM `geodata` WHERE `latitude`is NULL OR `longitude` is NULL)'
cursor = cnx.cursor()
cursor.execute(query)

# get phone numbers and addresses
phones = []
addresses = []
rows = cursor.fetchall()
for content in rows:
    phones.append(content[1])
    addresses.append(content[2] + " " + "Queens" + " " + content[4] + " " + content[5])

# get geo data for each row
cursor2 = cnx.cursor()
for a, p in zip(addresses, phones):
    location = geocoder.google(a, timeout=20)

    latitude = location.lat
    longitude = location.lng

    cursor2.execute('UPDATE `geodata` SET `latitude`={},`longitude`={} WHERE `phone`=\'{}\''.format(latitude, longitude, p))
    print('added ', p, latitude, longitude)
    
# commit changes and clean up
cnx.commit()
cursor.close()
cursor2.close()
cnx.close()