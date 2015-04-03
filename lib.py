#
#
#This is the main libray for PyScore
#
#

#Load required things
from mod_python import apache, util, Session
import MySQLdb
import hashlib

def mysql_password(str):
    #This function is identical to the MySQL PASSWORD() function.
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
	
def Connect_To_Database(req=None):
      
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
    try:
         util.redirect(req, "/")
    except:
         return  conn

def Get_Total_Points(session):

    #get the connection information for DB
    user = session['login']
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
    try:
         util.redirect(req, "/")
    except:
         return total_points[0]

def Print_Header(req):
    
    session = Session.Session(req)
    
    try:
        user_name = session['login']

    except:
        user_name = ""


    #print the header for navigation
    req.content_type = "text/html"
    req.write('<header>')
    req.write('    <link rel="stylesheet" href="/css/bootstrap.min.css">')
    req.write('    <link rel="stylesheet" href="/css/sidebar.css">')
    req.write('    <script src="/js/bootstrap.min.js"></script>')
    req.write('    <title>Pyscore</title>')
    req.write('</header>')
    req.write('<body>')
    req.write("\n<script>\n")
    req.write("(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\n")
    req.write("(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n")
    req.write("m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n")
    req.write("})(window,document,'script','//www.google-analytics.com/analytics.js','ga');\n")
    req.write("ga('create', 'UA-47552412-6', 'auto');\n")
    req.write("ga('send', 'pageview');\n")
    req.write("</script>\n")  
    req.write('  <nav class="navbar navbar-inverse navbar-fixed-top">')
    req.write('      <div class="container">')
    req.write('        <div class="navbar-header">')
    req.write('          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">')
    req.write('            <span class="sr-only">Toggle navigation</span>')
    req.write('            <span class="icon-bar"></span>')
    req.write('            <span class="icon-bar"></span>')
    req.write('            <span class="icon-bar"></span>')
    req.write('          </button>')
    req.write('          <a class="navbar-brand" href="/">Challenges</a>')
    req.write('        </div>')
    req.write('        <div id="navbar" class="navbar-collapse collapse">')
    req.write('          <ul class="nav navbar-nav">')
    if user_name != "":
        req.write('            <li><a href="/lib.py/logout">Log Out</a></li>')
    else:
        req.write('            <li><a href="/login">Log In</a></li>')
    req.write('            <li><a href="/score">Score Board</a></li>')
    if user_name == "":
        req.write('            <li><a href="/register">Register</a></li>')
    req.write('          </ul>')
    req.write('        </div><!--/.navbar-collapse -->')
    req.write('      </div>')
    req.write('    </nav>')
    if user_name != "":
        req.write('  <div class="col-sm-3 col-sm-offset-1 blog-sidebar">')
        req.write('    <div class="sidebar-module sidebar-module-inset" style="position: fixed; left: 5px;">')
        req.write("      <h4>Logged in as: " + str(user_name) + "</h4>")
        req.write("      <p>Total Points: " + str(Get_Total_Points(session)).replace('L', '') + "</p>")
        req.write('    </div>')
        req.write('  </div>')
    
    msg = messages(session)

    req.write('<center><h3>' + msg  +  '</h3></center>')
    session['msg'] = 1
    session.save()
    
    return session

def Get_Challenges(session):
    
    #get the connection information for DB
    conn = Connect_To_Database()


    #open a connection to the DB server
    curs = conn.cursor()

    #execute a check to see if
    curs.execute("SELECT * FROM PS_Challenges")

    #catch the server response
    ans = curs.fetchall()
    
    #close connection to database
    curs.close()

    session['challenges'] = ans 
    session.save()


def logout(req):

    session = Session.Session(req)

    session.delete()

    util.redirect(req, "/")

def messages(session):
    
     try:
          msg = session['msg']

     except:
          msg = 1

     if msg == 1:
          return ""
     elif msg == 2:
          return "Username and Password Combination Invalid"
     elif msg == 3:
          return "Your username cannot contain the following characters \n-<\',>;\~`"
     elif msg == 4:
          return "You must enter a valid email address"
     elif msg == 5:
          return "A user with that name already exists"
     elif msg == 6:
          return "A user with that email already exists"
     elif msg == 6:
          return "Password cannot be blank"
     elif msg == 7:
          return "Challenge text is incorrect"
     elif msg == 8:
          return "Challenge has already been completed"
     elif msg == 9:
          return "Both Password Feilds must be the same"
     else:
          return "An unknown error occured"
