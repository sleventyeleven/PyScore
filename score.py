from mod_python import apache
from operator import itemgetter, attrgetter
import lib

def index(req):
#start registration process

    Print_Header(req)
	
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