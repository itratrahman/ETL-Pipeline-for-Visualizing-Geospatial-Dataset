##Import statements
import sqlite3
import json
import codecs

##Connecting to already written sqlite database by the name of "geodata"
conn = sqlite3.connect('geodata.sqlite')
##Creating the database cursor
cur = conn.cursor()

##SQL command to extract all the data fromt the locations table
cur.execute('SELECT * FROM Locations')

##Opening the file handler with utf codecs
fhand = codecs.open('where.js','w', "utf-8")

##Writing the opening of the JSON data
fhand.write("myData = [\n")

##A counter variable
count = 0

##Iterating through each row returned by the SQL query
for row in cur :

	##Extracting the data
    data = str(row[1])
	
	##Try block on the occassion if JSON parsing of the data possible
    try: 
	
		js = json.loads(str(data))
		
	##Skip the iteration if JSON parsing is not possible
    except: 
	
		continue
	##Skip the iteration if the "status" of the JSON data doesnt exist or not "OK"
    if not('status' in js and js['status'] == 'OK') : 
	
		continue

	##Extracting the lattitude and longitude data from the JSON	
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
	
	##Skip the iteration if the lattitude or longitude is zero
    if lat == 0 or lng == 0 : 
	
		continue
		
	##Extract the formatted address			
    where = js['results'][0]['formatted_address']	
    where = where.replace("'","")
	
	
    try :
	
		##Print out the formatted address, lattitude, longitude
        print where, lat, lng

		##Increment the counter variable
        count = count + 1
		
		##Appending a new line if a data already exists in the JSON
        if count > 1 : 
		
			fhand.write(",\n")
		
		##Appening the location information to the JSON
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"		
        fhand.write(output)
	
	##Except block to skip the iteration if writing is not possible	
    except:
	
        continue

##Appending the closing of the JSON file
fhand.write("\n];\n")

##Closing the database cursor
cur.close()

##Closing the file handler
fhand.close()

##Printing the instruction statements
print count, "records written to where.js"
print "Open where.html to view the data in a browser"
