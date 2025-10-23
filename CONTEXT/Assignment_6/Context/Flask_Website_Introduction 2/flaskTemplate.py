'''
###################################################################################
Step 1: Did you create a virtual environment?
#-----------------------------------------------
# - View | Command Palette | Python: Create Environment
# = Select the type of environment you want to create (Venv, Conda, etc.)
# - Select the version of Python you want to use

#--------------------------------------------------
# Step 2: Did you activate the virtual environment?
#--------------------------------------------------
# - Do you see a green(venv) in the terminal at the start of the prompt?
# - Yes? You are good to go!
# - No? 
#   - Close and reopen the terminal
#   - Yes? You are good to go!
#   - No? 
#       - Run the following command:
#       - If you are on Windows, run the following command:
#           - .\venv\Scripts\activate.bat
#       - If you are on Mac, run the following command:
#           - source venv/bin/activate

#--------------------------------------------------
# Step 3: Did you install Flask?
#--------------------------------------------------
# - pip install Flask


#----------------------------------------------------------------------------------
# Step 4: Did you install any other dependencies needed? (don't need to do this)
#----------------------------------------------------------------------------------

#--------------------------------------------------
# Step 5: Let's make this easier for next time...
#-----------------------------------------------
# - In the terminal, type the following command:
# - pip freeze > requirements.txt
# - What did this do?
#   - It created a file called requirements.txt
# - What does requirements.txt do?
#   - It's a list of all the dependencies that are installed in the virtual environment
# - How do you use it?
#   - When you create a new virtual environment, if there is a requirements.txt file, 
#     you can use it to install the dependencies. As you go through the Create Environment
#     process, you can select the requirements.txt file to install the dependencies on one of the steps.
#----------------------------------------------------------------------------------
###################################################################################
'''

'''
#########################
# How to run the program
#########################
#-----------------------------------------------
# Option 1: Name this file app.py or wsgi.py
#-----------------------------------------------
# In the terminal, type the following command:
# flask run

#-----------------------------------------------
# Option 2: Name the file anyting you want and type (do NOT include the .py file extension)
#-----------------------------------------------
# In the terminal, type the following command:
# flask --app filename run

#-----------------------------------------------
# Option 3: Run the app in DEBUG mode
#-----------------------------------------------
# flask --app filename run --debug

#-----------------------------------------------
# Option 4: Add the following to the bottom of the program and then type python filename.py in
#           the terminal to run the website
#-----------------------------------------------
# if __name__=='__main__':
#     app.run(debug=True)

#### NOTE: ####
# When you run this file, there will be no website because we do not have any "routes" or "pages" to go to.
# After running the file, you will need to press CTRL + C to stop the server.
'''

# 1.  Import the Flask library. This is a web framework (aka web server)
from flask import Flask

# 2. Create a instance of the Flask() class with the only parameter being
#    a "system" variable called __name__. If you want to see what is in __main__
#    create a new Python program file and print it and see what it prints.
#    Call the instance/object "app"
app = Flask(__name__)


# Write your webpages here ...






# Write code to allow us to type python flaskTemplate.py
if __name__=='__main__':
    #app.run()
    app.run(debug=True)