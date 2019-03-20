# Item Catalog Web App
By PAVANKUMAR KOTHAGUNDU
This web app is a project for the Udacity Full Stack Nano Degree.


## About
This Project provides Authorization and Authentication to user.
It is a Web Application which provides a list of items within different categories as well as provide a user registration and authentication system. The Registered users will have the ability to add, update and delete their own items.

## Project Structure

--> __pycache__
	a)Data_Setup.cpython-37
	
--> static
	a)styles.css(CSS File)
	
--> templates
	This Folder Contains The Following HTML Files
	a)addBoatCompany
	b)addBoatDetails
	c)admin_login
	d)admin_loginFail
	e)deleteBoat
	f)deleteBoatCategory
	g)editBoat
	h)editBoatCategory
	i)login
	j)mainpage
	k)myhome
	l)nav
	m)showBoats
	
--> venv (Virtual Environment)
	a)Include
	b)Lib
	c)Scripts
	d)tcl
	The above files are related to virtual environment
	
--> boats.db

--> client_secrets.json
	This File Consists "client_id" and "client_secret" which is used in Authentication of Our Google Account
	
--> Data_Setup.py
	This is the python file in which the database as well as the tables with columns are created.

--> database_init.py
	This is the python file which is used to enter the data into the columns of the table in the database.

--> main.py
	This is the python file Which gives the internal configuration of the project such as adding, editing and deleting of categories as well as items in the categories.

-->README.md
	This Shows the entire Working Of the Project.


## Skills & Tools Required

1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
7. Vagrant
8. VirtualBox


## How to Run

1. In First Step we have to Install Vagrant.
2. Now We have to Install VirtualBox.
3. Then Open CommandPrompt in your Folder's Path.
4. First initialize the Vagrant using the command:
	$ vagrant init ubunti/xenial64
5. Launch Vagrant Using the Command
	$ vagrant up
6. Log into Vagrant using Command
	$ vagrant ssh
7. Change the directory to vagrant using command
	$ cd vagrant
8. The app imports requests which is not on this vm. Run pip install requests
9. Now we have to activate the Virtual Environment in our Folder by Using the Command
	$ venv\scripts\activate
10. Run the Data_Setup.py using the command
	$ python Data_Setup.py
	 Execution of this file leads to creation of a database file(boats.db) 
11. Run the database_init.py using the command
	$ python database_init.py
	Execution of this file leads to insertion of data into the database file
12. And then Run the main.py using the command 
	$python main.py
	This File Executes the entire Project including Templates and remaining files
13. Access the application locally using http://localhost:8000	
	By running running main.py file in command prompt the server of our project will activates and we have to type the above url in browser.This displays basic version of our project.
14. Here we cannot be able to edit,add,delete our items.To enable edit,add,delete options we have to login to our 
	account.

## Using Google Login
	To Work in our Project we need to follow these steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Boat Sale Company'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Finally Run The Project using the steps mentioned in ## How to Run.
14. Now you can add,update and delete the Items in our Project.

## JSON Endpoints
The following are open to the public:

Boats Catalog JSON: `/BoatsStore/JSON`
    - Displays the whole boat models catalog. Boat Categories and all models.

Boat Categories JSON: `/boatsStore/boatCategories/JSON`
    - Displays all Boat categories
	
All Boat Editions: `/boatsStore/boats/JSON`
	- Displays all Boat Models

Boat Edition JSON: `/BoatsStore/<path:boatcompanyname>/boats/JSON`
    - Displays Boat models for a specific Boat category

Boat Category Edition JSON: `BoatsStore/<path:boatcompanyname>/<path:edition_name>/JSON`
    - Displays a specific Boat category Model.

