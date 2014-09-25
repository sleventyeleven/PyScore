from mod_python import apache
import MySQLdb
import hashlib

def index(req):
#start registration process

    req.content_type = "text/html"
    req.write('<link rel="stylesheet" href="../format.css" type="text/css" />')
    req.write("<p><html>")
    req.write('<form action="register.py/register" method="POST">')
	req.write("Do not lose this information!")
	req.write("THERE IS NOT METHOD OF RECOVERY!!!!")
    req.write('<input type="text" name="User Name"><br>')
    req.write('<input type="text" name="Password"><br>')
    req.write('<input type="submit">')
    req.write("</form></html>")

def mysql_password(str):
    #This function is identical to the MySQL PASSWORD() function.
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
	
def Connect_To_Database():
#get the settings file and read it in

    try:
        settings_file = open("../settings.ini", 'r')

    except IOError:

        path_to_settings_file = raw_input("Please enter the full path to the settings.ini file: ")
        settings_file = open(path_to_settings_file, 'r')



    #read settings form the file

    for line in settings_file:

        settings = []

        settings = line.split("=")
        
        if settings[0] == "UserName":
            setting_user_name = settings[1]
        elif settings[0] == "Password":
			setting_password = setting[1]
		elif settings[0] == "Database":
			setting_database = setting[1]
		elif settings[0] == "Host":
			setting_host = setting[1]
		else:
			print "I don't understand parsed setting"
	
    #connect to the Database
    conn = MySQLdb.connect(host=setting_host, user=setting_user_name, passwd=setting_password, db=setting_database)
    #return the connection settings
    return conn
	
def register(req, name, password):

    user_password = mysql_password(password)
	
	user_name = mysql_password(name)
	
	defualt_score = 0

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

    if user_name or user_password in users:
        return '<meta http-equiv="refresh" content="0;url=/register/">'
	
	else
	    #open a connection to the DB server
        curs = conn.cursor()
	
	    #execute a check to see if
        curs.execute("INSERT INTO PS_Users (User_Name, User_Password, Total_Points) VALUES (%s,%s,%s)",(user_name, user_password, defualt_score))
		
		#commit and close connection to database
        conn.commit()
        curs.close()
        return '<meta http-equiv="refresh" content="0;url=/">'