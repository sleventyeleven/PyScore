from mod_python import apache
from operator import itemgetter, attrgetter
from lib import *

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
 
    req.write("<p>")
    req.write("<center><h1>Score Board</h1></center>")
    req.write('<div class="col-sm-4 center-table">') 
    req.write('<table class="table">')
    req.write('<thead>')
    req.write('<tr>')
    req.write('<th>#</th>')
    req.write('<th>Username</th>')
    req.write('<th>Points</th>')
    req.write('</tr>')
    req.write('</thead>')
    req.write('<tbody>')   

    sorted_users = sorted(users, key=itemgetter(2), reverse=True)
	
    counter = 0
    for user in sorted_users:
         counter += 1
         
         req.write('<tr>')
         req.write('<td>' + str(counter) + '</td>')
         req.write('<td>' + str(user[0]) + '</td>')
         req.write('<td>' + str(user[2]) + '</td>')
         req.write('</tr>')

    req.write('</center></tbody>')
    req.write('</table>')
    req.write('</div>')	
    return apache.OK
