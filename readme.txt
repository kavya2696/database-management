This project consists of a simple web application built using Flask for the backend and HTML, CSS, and JavaScript for the frontend. It allows users to view, update and delete records in a database.

INSTALLATION:

1. Python
	--> Link for python installation:
		--> https://realpython.com/installing-python/
	--> Requires python 3.5 or higher

2. Zorba
	--> Link for zorba installation:
		--> http://www.zorba.io/home

3a. Cx-Oracle
	--> Link for cx_Oracle Installation:
		--> https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

3b. Oracle Instant Client
	-->Link for Oracle Instant Client:
		--> https://www.oracle.com/database/technologies/instant-client/downloads.html
	--> Install the BASIC PACKAGE

4a. flask
	-->pip install Flask

4b. Flask-cors
	-->pip install flask-cors

Description:
Frontend
1. HTML (index.html):

This file provides the structure of the frontend. It includes forms to create, update and delete records. Make sure to place this file in the templates directory.

2. CSS (styles.css):

The CSS file provides styling for the HTML elements in the frontend. Ensure this file is in the static/ folder.

3. JavaScript (app.js):

JavaScript is used to make GET,POST and DELETE requests to create, update and delete records. Place the app.js file in the static/ folder.

4. Python (app.py):
The python file is the core of this Flask web application. It acts as the backend, handling HTTP requests, performing database operations, and serving data to the front-end. 

Running the Application:
1. In terminal, navigate to folder and run the Flask server
	python app.py
2. Once your backend and frontend are set up, and the Flask server is running, Open your browser and navigate to 
	http://127.0.0.1:5000/
3. You will see a webpage with forms for fetch the records from database.
4. You can interact with the page, fetch the records, update the existing records and also delete the records of the items, business entity, Bill of Materials, Supplier Discounts, Supply Unit Pricing, Manufacturer Discounts, Manufacturer Unit Pricing, Shipping Pricing, Customer Demand, Supply Orders, Manufacturer Orders, Shipping Orders tables in the Oracle database via the Flask backend.