# A. Import the sqlite library
import sqlite3

#######################################################
# 1. ADD MOVIE TO DB
#######################################################
def saveMovieDB(Title, Year, ImageName):
    #A. Make a connection to the database
    conn = None
    conn = sqlite3.connect( "movies.db")

    #B. Write a SQL statement to insert a specific row (based on Title name)
    sql='INSERT INTO movies (Title, YearReleased, ImageName) values (?,?,?)'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it 1 parameter for each ?
    cur.execute(sql, (Title,Year,ImageName, ))

    # D. Save the changes
    conn.commit()
    if conn:
        conn.close()

#######################################################
# 2.  SHOW MOVIES IN A TABLE
#######################################################
#   THIS RETURNS AS LIST OF DICTIONARIES
def getAllMovies():
    # A. Connection to the database
    conn = sqlite3.connect('movies.db')

    # B. Create a workspace (aka Cursor)
    cursorObj = conn.cursor()

    # D. Run the SQL Select statement to retive the data
    cursorObj.execute('SELECT Title, YearReleased, ImageName FROM Movies;')

    # E. Tell Pyton to 'fetch' all of the records and put them in
    #     a list called allRows
    allRows = cursorObj.fetchall()

    movieListOfDictionaries = []

    for individualRow in allRows:
        # Make sure we have an image name
        if individualRow[2] is not None and individualRow[2] != "":
            Image = individualRow[2]
        else:
            Image = "placeholder.png"
        # Create a dictionary for each row
        m = {"Title" : individualRow[0], "Year": individualRow[1], "Image":Image}
        movieListOfDictionaries.append(m)

    if conn:
        conn.close()

    return movieListOfDictionaries
