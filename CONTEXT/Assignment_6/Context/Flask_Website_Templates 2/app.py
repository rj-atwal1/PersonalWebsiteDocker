###############################################################################
#                         IMPORT REQUIRED LIBRARIES/MODULES
###############################################################################
from flask import Flask #The FLASK framework (the webserver)
from flask import render_template  # For opening and read the HTML file and showing them as the webpage
from flask import request  #Allows me to get stuff from the URL (the ?)

from flask import redirect, url_for # Use images from the static folder

app=Flask(__name__)

@app.route("/")         # Decorator - Place above any other app.route to set "homepage"
@app.route("/page1")    # Decorator - Alias for the homepage (aka page1)
def page1():
    return render_template('page1.html')

@app.route("/legal")    # Decorator - Alias for the legal page (aka page2)
@app.route("/page2")    # Decorator - Alias for the page2   
def page2():
    #Let's send some date to page2.html.

    # 1. We will store the data in a list called mList
    mList = [] #Create an empty list
    #2. Let's add a couple of Dictionaries to the list
    mList.append({
                    'FirstName':"Jay",
                    'LastName':"Newquist"
                    })
    mList.append({
                    'FirstName':"Vijay", 
                    'LastName':"Khatri"
                    })
    titleText = "This will be a subtitle"
    return render_template('page2.html',
                            message_list=mList , # IMPORTANT!: message_list is the name of the list in the template
                            title=titleText )    # IMPORTANT!: title is the name of the variable in the template


@app.route("/page3")    # Decorator - Alias for the page3 page (aka page3)
@app.route("/aboutus")    # Decorator - Alias for the aboutus page (aka page3)
def page3():
    return """
            <html>
                <head><title>Page 3</title></head>
                <body>
                    <h1>Welcome to Page 3</h1>
                    No template for this 'page'. <br>
                    <a href='page1'>Page 1</a><br />
                </body>
            </html>
            """

app.run(debug=True)