Bus Tracking System API - 1.4
-------------------------
Change Log : enabled CORS. added /busgeofence. updated /geofence. 
-------------------------
The Rest API has been deployed to AWS
.
Link: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com

Everybody can use the below endpoints to access the tabbles in the database.

/register - POST into Users table
/login - takes a JSON object with 'username' and 'password' and gives back JWT if exists in Users table.
	 The JWT shall be used to access all the end points.
	 For all the endpoints an Authorization Header should be included with value 'Bearer <JWT>'.
/tracking (POST) - POST into Rawdata table
/tracking (GET) - takes a JSON object with 'routeId' and 'deviceTime' to give back Livedata with respect to input.
			routeId==None and deviceTime==None:
				returns Livedata of all Buses
			routeId!=None and deviceTime==None:
				returns Livedata of given routeId
			routeId!=None and deviceTime!=None:
				returns Tracking of given routeId at given deviceTime	

/sms - sends SMS in bulk. takes a JSON object with 'to' and 'message'.
	if 'to'=='users': given message is sent to all Users.
	if 'to'=='drivers': given message is sent to all Drivers.
/geofence (POST) - POST into Geofence table.
/geofence (GET) - takes a JSON object with 'routeId','fromDate','toDate','status'.
		  'fromDate' and 'toDate' are must.
		  if 'routeId' is given, data related only to that 'routeId' is returned else everything is returned.  	

		  if 'status' is given, data with given status only is returned else everything is returned.
/busgeofence (POST) - POST into BusGeofence table.
/busgeofence (DELETE) - takes a JSON object with 'routeId' and deletes all the rows from BusGeofence table with the given 'routeId'.
/busgeofence (GET) - takes a JSON object with 'routeId' and returns a list of latitudes and logitudes detetrmining bus geofence.
		     if 'routeId' is not given, returns a list of latitudes and logitudes detetrmining bus geofence for all routes.
/buses - Bus table

/routes - Routes table

/drivers - Driver table

/sos - Sos table

/alerts - AlertsControl table

/users - Users table

Example: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com/routes

All the endpoints returns the data as a list of dictionaries in JSON format which can be converted and used in the program directly.
