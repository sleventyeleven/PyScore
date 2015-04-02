from mod_python import apache, Session, util
from lib import *
import time

def index(req):
#start registration process

    Print_Header(req)
    
    req.write('<link rel="stylesheet" href="/css/login.css">')
    req.write('<div class="container">')
    req.write('<form class="form-signin" action="/login.py/login" method="POST">')
    req.write('<h2 class="form-signin-heading">Please Sign In</h2>')
    req.write('<label for="text" class="sr-only">Username</label>')
    req.write('<input type="text" name="username" id="username" class="form-control" placeholder="Username" required>')
    req.write('<label for="inputPassword" class="sr-only">Password</label>')
    req.write('<input type="password" name="password" id="inputPassword" class="form-control" placeholder="Password" required>')
    req.write('<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>')
    req.write("</form></html>")

	
def login(req, username, password):

    session = Session.Session(req)
    
    pw = mysql_password(password)
    
    if pw == "*BE1BDEC0AA74B4DCB079943E70528096CCA985F8":
        session['msg'] = 6
        session.save()
        util.redirect(req, "/login")

    #get the connection information for DB
    conn = Connect_To_Database()
   
    #open a connection to the DB server
    curs = conn.cursor()

    #get a list of users
    curs.execute("SELECT * FROM PS_Users")

    users = curs.fetchall()
    curs.close()

    counter = 0
    for user in users:

        if user[0] == username and user[1] == pw:
            session['login'] = username
            session.save()
            util.redirect(req, "/")

    session['msg'] = 2
    session.save()
    util.redirect(req, "/login")
