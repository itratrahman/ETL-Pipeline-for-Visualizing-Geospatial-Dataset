
####Import Statements
import urllib ##Importing the URL library
import sqlite3 ##Importing the sqlite3 library
import json ##Importing the json library
import time ##Importing the time library

##Service URL of GOOGLE
serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

scontext = None

##Creating a sqlite3 database by the name of 'geodata'
conn = sqlite3.connect('geodata.sqlite')

##Creating the database cursor
cur = conn.cursor()

##SQL command to create a Locations table in the database
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')
				
##File handler for the file "where.data"
fh = open("where.data")

##A counter variable
count = 0

##Iterating through each line in the file
for line in fh:

	##if statement to break off the loop if the count exceeds 200
	if count > 200 : 
		break
	
	##Stripping the line of new line character	
	address = line.strip()
	print ''
	
	##A SQL query to select geodatalocation retrieved from the current line of the file
	cur.execute("SELECT geodata FROM Locations WHERE address= ?", (buffer(address), ))
	
	##Try block to skip the iteration in the case when SQL command gives a column, 
	#meaning the database already has that location
	try:
		data = cur.fetchone()[0]
		
		print "Found in database: ", address
		
		continue
	
	##Continue retrieving location information if data is not in the database
	except:
		
		pass
		
	print "Resolving", address
	
	##URL encoding the address and appending it to the service url
	url = serviceurl + urllib.urlencode({"sensor":"false", "address": address})
	
	print "Retrieving", url
	
	##Opening and reading the URL content
	uh = urllib.urlopen(url, context=scontext)
	data = uh.read()
	
	##Print out some retrieved data
	print "Retrieved", len(data), 'characters', data[:20].replace('\n',' ')
	
	##Increment the counter variable
	count = count + 1
	
	##Try block to deal with case when json retrieval is possible
	try:
		
		##Jasonifying the data
		js = json.loads(str(data))
		
	##skip the iteration on failure to parse the data
	except:
	
		continue
		
	##Print status and break statement on the event of retrieval failure
	if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : 
	
		print "==== Failure To Retrieved ===="
		
		print data
		
		break
	
	##Inserting the location and location info into the database	
	cur.execute('''INSERT INTO Locations (address, geodata) 
            VALUES ( ?, ? )''', ( buffer(address),buffer(data) ) )
			
	##Committing the update into database
	conn.commit() 
	
	##Sleeping for more data to arrive
	time.sleep(1)
	
print "Run geodump.py to read the data from the database so you can visualize it on a map."	
		


