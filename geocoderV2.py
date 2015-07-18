import time
import mysql.connector
import geocoder

cnx = mysql.connector.connect(user='root', 
                              password='root',
                              host='127.0.0.1',
                              database='flushingfood')


cursor = cnx.cursor()
query = 'SELECT * FROM `restaurants` WHERE `phone` IN (SELECT `phone` FROM `geodata` WHERE `latitude`is NULL OR `longitude` is NULL)'
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
cnx.close()

addresses = []
names = []
phones = []
for content in rows:
    names.append(content[0])
    phones.append(content[1])
    addresses.append(content[2] + " " + "Queens" + " " + content[4] + " " + content[5])

print(len(phones))
for a, n, p in zip(addresses, names, phones):
    location = geocoder.google(a, timeout=20)

    if location is not None:
        print('{:15s}'.format(p), '{:25s}'.format(n), (location.lat, location.lng))
    else:
        print(n, 'ADDRESS IS WRONG')