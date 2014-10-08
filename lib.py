#
#
#This is the main libray for PyScore
#
#

#Load required things
import MySQLdb
import hashlib

def mysql_password(str):
    #This function is identical to the MySQL PASSWORD() function.
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
	
def Connect_To_Database():
    #get the settings file and read it in

    settings_file = open("/var/www/settings", 'r')

    #read settings form the file

    for line in settings_file:

        settings = []

        settings = line.split("=")
        
        if settings[0] == "UserName":
            setting_user_name = settings[1].strip("\n")
        elif settings[0] == "Password":
            setting_password = settings[1].strip("\n")
        elif settings[0] == "Database":
            setting_database = settings[1].strip("\n")
        elif settings[0] == "Host":
            setting_host = settings[1].strip("\n")
        else:
            print "I don't understand parsed setting"
	
    #connect to the Database
    conn = MySQLdb.connect(host=setting_host, user=setting_user_name, passwd=setting_password, db=setting_database)
    #return the connection settings
    return conn
	
    if user_name or user_password in users:
        return '<meta http-equiv="refresh" content="0;url=/register/">'
	
    else:
	#open a connection to the DB server
        curs = conn.cursor()
	
	#execute a check to see if
        curs.execute("INSERT INTO PS_Users (User_Name, User_Password, Total_Points) VALUES (%s,%s,%s)",(user_name, user_password, defualt_score))
		
        #commit and close connection to database
        conn.commit()
        curs.close()
        return '<meta http-equiv="refresh" content="0;url=/">'

def Auth_User():
    def __auth__(req, user, password):
        
        global user_name
        user_name = user
        pw = mysql_password(password)
    
        #check for null or none password
        if pw == "*BE1BDEC0AA74B4DCB079943E70528096CCA985F8":
            return 0
    
        #get the connection information for DB
        conn = Connect_To_Database()
    
        #open a connection to the DB server
        curs = conn.cursor()
    
        #clean user input
        user = user.replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "")
    
        #execute a check to see if
        curs.execute("SELECT User_Password FROM PS_Users WHERE User_Name =%s",(user))
    
    
        #catch the server response
        mysql_pw = curs.fetchone()
    
        #check for bad user
        if mysql_pw == None:
            curs.close()
            return 0
    
    
        if pw == mysql_pw[0]:
           curs.close()
           return 1
        else:
           curs.close()
           return 0

def Get_Total_Points(user):

    #get the connection information for DB
    conn = Connect_To_Database()

    #open a connection to the DB server
    curs = conn.cursor()

    #execute a check to see if
    curs.execute("SELECT Total_Points FROM PS_Users WHERE User_Name =%s",user)

    #catch the server response
    total_points = curs.fetchone()

    #close connection to database
    curs.close()

    #return the users total points
    return total_points[0]

def Print_Header(req):

    #print the header for navigation
    req.content_type = "text/html"
    req.write('<link rel="stylesheet" href="../format.css" type="text/css" />')

    if user_name != "":
        req.write("Logged in as: " + str(user))
        req.write("<p>")
        req.write("Total Points: " + str(Get_Total_Points(user)).replace('L', ''))
        req.write("<p>")

    req.write('<a href="/register">Register</a>')
    req.write('<a href="/score">Score</a>')
    req.write('<a href="/page">Summit</a>')

