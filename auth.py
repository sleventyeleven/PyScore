from mod_python import apache
import MySQLdb
import hashlib

def authenhandler(req):

    pw = mysql_password(req.get_basic_auth_pw())
    user = mysql_password(req.user)
	
    #check for null or none password
    if pw == "*BE1BDEC0AA74B4DCB079943E70528096CCA985F8":
        return apache.HTTP_UNAUTHORIZED
    
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
        return apache.HTTP_UNAUTHORIZED
    
    
    if pw == mysql_pw[0]:
       curs.close()
       return apache.OK
    else:
       curs.close()
       return apache.HTTP_UNAUTHORIZED
   
   
def mysql_password(str):
    #This function is identical to the MySQL PASSWORD() function.
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
	
def Connect_To_Database():
#get the settings file and read it in

    try:
        settings_file = open("settings.ini", 'r')

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
