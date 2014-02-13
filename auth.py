from mod_python import apache
import MySQLdb
import hashlib

def authenhandler(req):

    pw = mysql_password(req.get_basic_auth_pw())
    user = req.user
    
    #get the connection information for DB
    conn = Connect_To_Database()
    
    #open a connection to the DB server
    curs = conn.cursor()
    
    #execute a check to see if
    curs.execute("SELECT User_Password FROM PS_Users WHERE User_Name =%s",(user))
    
    #catch the server response
    mysql_pw = curs.fetchone()

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
    #connect to the Database
    conn = MySQLdb.connect(host="localhost", user="PyScore", passwd="P@ssw0rd", db="PyScore")
    #return the connection settings
    return conn
