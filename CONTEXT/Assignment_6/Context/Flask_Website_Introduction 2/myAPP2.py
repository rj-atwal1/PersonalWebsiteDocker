# NEW
#=====================================
# 1. ADD HTML to the output
# 2. CREATE & ADD a variable to the ouput
# 3. Add a virtual subfolder to one of the pages
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
    return """<html>
                <head>
                    <title>Jay's Homepage</title>
                </head>
                <body>
                    <H1>Welcome to Jay's Homepage</H1>
                    <p>
                        Take a rest and learn how to make webpages.
                    </p>
                    <!-- NOTE: We have to specify that the file is in the virtual subfolder -->
                    <a href="/subfolder/aboutme">About me</a>
                </body>
            </html>"""

# 5. Create another route (aka page) but this time put it in a virtual
#    subfolder called subfolder. Don't forget that when you link back to
#    the home page you have to tell Python that the home page is in the
#    parent folder.
@app.route("/subfolder/aboutme")
def secondPage():
    now = datetime.now()
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
                    <a href="../home">Go to home page!</a>
                </body>
            </html>
            """

if __name__=='__main__':
    #app.run()
    app.run(debug=True)