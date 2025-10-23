# NEW
#=====================================
# 1. Get a variable from the URL
# 2. Look at alternatives to moving in and out of
#    a virtual subfolder
# 3. Move the HTML to functions so that the code
#    is a bit easier to read
#=====================================

# 1.  Import the Flask library. This is a web framework (aka web server)
from flask import Flask

# 2. Bring in the datetime library so that we can run datetime code
from datetime import datetime

# 2. Create a instance of the Flask() class with the only parameter being
#    a "system" variable called __name__. If you want to see what is in __main__
#    create a new Python program file and print it and see what it prints.
#    Call the instance/object "app"
app = Flask(__name__)

# 3. We then use the route() decorator (aka function) to tell Flask what URL should trigger our function.
#    / means the root or "top" level
@app.route("/")     # Default page when you only type the Server URL
@app.route("/home") # Explicit name when you type the Server URL and the route name
# 4. Now let’s tell the website what we should send to the person's web browser who visited our page
def hello_world():
    return getHomePage()

# 5. Create another route (aka page)
@app.route("/aboutme")
def secondPage():
    now = datetime.now()
    return getaboutme(now)

# 6. Create another route (aka page) but this time ask for a name
#    You can get values from the URL by adding <variableName> to the app.routes
@app.route("/Name/<name>") # NOTE: THIS WILL BE IN A VIRTUAL SUBFOLDER DUE TO IT HAVING TWO SLASHES \ \
def thirdPage(name):
    # NOTE: We use %s as the placeholder in the HTML text below and we can use that place holder to
    #       swap in variable names (i.e. name from above)
    #       We add another % at the END of the HTML text as well.  We use that to indicate which
    #       variable (i.e. "name") to swap in for the %s place holder IN the HTML
    return  getNamePage() % name


#################################################
# NOTE
# Rather than writing all this HTML code above and making that code even HARDER to read.  Let's
#   build this webpages here...
#################################################

# Build the HOME page
def getHomePage():
    return """<html>
                <head>
                    <title>Jay's Homepage</title>
                </head>
                <body>
                    <H1>Welcome to Jay's Homepage</H1>
                    <p>
                        Take a rest and learn how to make webpages.
                    </p>
                    <a href="aboutme">About me</a>
                </body>
            </html>"""

# Build the about me page but PASS the time to it first as a parameter
def getaboutme(now):
    return """
            <html>
                <head>
                    <title>Jay's About Me Page</title>
                </head>
                <body>
                    <H1>Welcome to Jay's About Me Page.</H1>
                    <p> Today's Date and Time is """ + str(now) + """
                        <br />Type something interesting about yourself.
                        <br /><br />
                    <a href="Name/ChangeThisToYourName">Go to name page!</a>
                </body>
            </html>
            """

# Build the Name page. NOTE: go ahead and put the %s into the string below. It can be swapped out above
def getNamePage():
    return """
            <html>
                <head>
                    <title>Name Page</title>
                </head>
                <body>
                    <!-- Notice the placeholder in the line below (percentage s)  -->
                    <H1>Welcome to %s's About Me Page.</H1>
                        <br />This page should be showing you your name.  If it is not, overwrite the ChangeThisToYourName
                        in the above address bar to your name so that it displays in the page.
                        <br /><br />
                    <a href="/home">Go to home page</a> This link will work...
                    <br /><br />
                    <a href="../home">Go to home page</a> This link will also work...
                    <br /><br />
                    <a href="home">Go to home page</a> Why does this link not work? And why is the name now home's
                    <br />Take a closer look at the / (forward slash) in the href of the link that works? Why is it needed?
                </body>
            </html>
            """

# Write code to start up your website
if __name__=='__main__':
    #app.run()
    app.run(debug=True)