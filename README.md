Bus Tracking System - 1.1
-------------------------
using waitress module for WSGI production server.
-------------------------
The Rest API has been deployed to AWS
.
Link: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com

Everybody can use the below endpoints to access the tabbles in the database.

/tracking - Rawdata table

/buses - Bus table

/routes - Routes table

/drivers - Driver table

/sos - Sos table

/alerts - AlertsControl table

/users - Users table

Example: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com/routes

All the endpoints returns the table data as a list of dictionaries in JSON format which can be decrypted and used in the program directly.
