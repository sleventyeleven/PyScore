from mod_python import apache
import MySQLdb
import hashlib
from operator import itemgetter, attrgetter

def index(req):
#start registration process

    #set content type to html
    req.content_type = "text/html"
	
    #get the connection information for DB
    conn = Connect_To_Database()
    
    #open a connection to the DB server
    curs = conn.cursor()
	
    #execute a check to see if
    curs.execute("SELECT * FROM PS_Users")
	
    #catch the server response
    users = curs.fetchall()

    #close connection to database
    curs.close()

    req.content_type = "text/html"
 
    req.write("<p><html>")
    req.write("<p>Score Board <p>")
	
    sorted_users = sorted(users, key=itemgetter(2), reverse=True)
	
    counter = 0
    for user in sorted_users:
         counter += 1
         req.write("<p>" + str(counter) + ". " + str(user[0]) + " with "  + str(user[2]) + " points")
	
    return apache.OK

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
