This is an ETL pipeline that retrieves geodata from Google Map API, cleans the data and store the cleaned data in database and then visualize them on a map.

geoload.py loads raw data of places stored in the where.data file. It then retrieves the geodata of such places, and stores them in a two column database "geodata.sqlite". One column to store the places and the other to store the JSON retrieved from Goolge Map API.

geodump.py extracts a subset of the geodata namely, longitude, lattitude, and formatted address, of places from the JSON data stored in the database and forms a long JSON "myData" in file "where.js".

where.html use Google Map for visualization of the places.