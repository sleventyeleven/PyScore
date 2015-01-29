from mod_python import apache, util, Session
from lib import *

def index(req):
#start registration process

    Print_Header(req)
    
    req.write('<link rel="stylesheet" href="/css/login.css">')
    req.write('<div class="container">')
    req.write('<form class="form-signin" action="/register.py/register" method="POST">')
    req.write('<h2 class="form-signin-heading">Required Information</h2>')
    req.write("<h5>Do not lose this information!</h5>")
    req.write("<h3>THERE IS NO METHOD OF RECOVERY!!!!</h3>")
    req.write('<label for="text" class="sr-only">Username</label>')
    req.write('<input type="text" name="username" id="username" class="form-control" placeholder="Username" required>')
    req.write('<label for="inputEmail" class="sr-only">Email address</label>')
    req.write('<input type="inputEmail" name="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>')
    req.write('<label for="inputPassword" class="sr-only">Password</label>')
    req.write('<input type="password" name="password1" id="inputPassword" class="form-control" placeholder="Password" required>')
    req.write('<label for="inputPassword" class="sr-only">Password</label>')
    req.write('<input type="password" name="password2" id="inputPassword" class="form-control" placeholder="Repeat Password" required>')
    req.write('<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>')
    req.write("</form></html>")

	
def register(req, username, email, password1, password2):

    if password1 == password2:
        user_password = mysql_password(password1)
    else:    
        util.redirect(req, "/register")
    user_name = str(username).replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "")
    user_email = str(email).replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "")

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

    if user_name in users:
        util.redirect(req, "/register")
	
    else:
	#open a connection to the DB server
        curs = conn.cursor()
	
	#execute a check to see if
        curs.execute("INSERT INTO PS_Users (User_Name, User_Password, Total_Points, User_Email) VALUES (%s,%s,%s,%s)",(user_name, user_password, defualt_score, user_email ))
		
        #commit and close connection to database
        conn.commit()
        curs.close()

        session = Session.Session(req)
        session['login'] = user_name
        session.save()
        util.redirect(req, "/")

