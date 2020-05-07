Bus Tracking System - 1.2
-------------------------
Change Log : added /login. added Authentication using JWT. modified /tracking. DB error rectified.
-------------------------
The Rest API has been deployed to AWS
.
Link: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com

Everybody can use the below endpoints to access the tabbles in the database.

/login - takes a JSON object with username and password and gives back JWT if valid.
	 The JWT shall be used to access all the end points.
	 For all the endpoints an Authorization Header should be included with value 'Bearer <JWT>'.
/tracking - takes a JSON object with routeId and deviceTime to give back Tracking data with respect to input.
		routeId==None and deviceTime==None:
			returns Livedata of all Buses
		routeId is not None and deviceTime==None:
			returns Livedata of given routeId
		routeId==None and deviceTime is not None:
			returns Tracking of all Buses at given deviceTime
		routeId is not None and deviceTime is not None:
			returns Tracking of given routeId at given deviceTime	


/buses - Bus table

/routes - Routes table

/drivers - Driver table

/sos - Sos table

/alerts - AlertsControl table

/users - Users table

Example: ec2-3-7-131-60.ap-south-1.compute.amazonaws.com/routes

All the endpoints returns the table data as a list of dictionaries in JSON format which can be decrypted and used in the program directly.
