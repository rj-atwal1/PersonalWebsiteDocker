###############################################################################
#                         IMPORT REQUIRED LIBRARIES/MODULES
###############################################################################
# 1. The FLASK framework (the webserver)
from flask import Flask

# 2. For opening and read the HTML file and showing them as the webpage
from flask import render_template

# 3. From the flask library import the request class.
# Allows us to get information from the website URL
from flask import request

# 4. Import the objects.py file
from DAL import *

# 5. Import the sqlite library
# SQLITE is NOT imported here. I do not have any SQL in this file
# import sqlite3

# 6. Instantiate the Flask() class and called it app
app=Flask(__name__)

###############################################################################
#                         CREATE YOUR WEBPAGE ROUTES
###############################################################################

#------------------------------------------------------------------------------------
# C) Create a page to INSERT records
#------------------------------------------------------------------------------------
@app.route("/")
@app.route("/add", methods=["GET","POST"]) # Decorator - Now
def add():
    if request.method == "GET":  # When you first visit the page

        # C1) Run a method called getAllMovies().  Instaniation is not needed.
        mList=getAllMovies()
        return render_template('add.html',message=mList)

    elif request.method == "POST": # When you fill out the form and click SUBMIT
        # C1) Run a method called getAllMovies().  Instaniation is not needed.
        mList=getAllMovies()

        # Get the value from the form object called "movtitle" (it is a textbox)
        title = request.form.get("movtitle", 0)

        # Get the value from the form object called "movyear" (it is a textbox)
        # This is an INTEGER. Quick, change it from TEXT to INTEGER using int() function
        year = int(request.form.get("movyear", 0))

        # Get the value from the form object called "movtitle" (it is a textbox)
        ImageName = request.form.get("ImageName", 0)

        # Run the function called saveMovieDB passing the method the title of the movie
        #   and the year the movie was release
        saveMovieDB(title, year, ImageName)

        # C1) Run a method called getAllMovies().  Instaniation is not needed.
        mList=getAllMovies()

        #Return the template index.html but pass it the list of movies
        # stored in the variable mList
        return render_template('add.html',message=mList )

    else:
        # How could it have not been a GET or POST? I have no idea how that could have happened.
        return render_template('add.html',message='Something went wrong.')


app.run(debug=True)