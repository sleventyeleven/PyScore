from mod_python import apache, util, Session
from lib import *
import recaptchalib
def index(req):
#start registration process

    Print_Header(req)
    
    req.write('<link rel="stylesheet" href="/css/login.css">')
    req.write("<script src='https://www.google.com/recaptcha/api.js'></script>")
    req.write('<div class="container">')
    req.write('<form class="form-signin" action="/register.py/register" method="POST">')
    req.write('<h2 class="form-signin-heading">Required Information</h2>')
    req.write("<h5>Do not lose this information!</h5>")
    
    # Recaptcha stuff
    site_key = "6LdT2gITAAAAAEnTL8_OaiIOli0I7H7-9MKhpanN"
    secret = "6LdT2gITAAAAAADb1Rae2QgcADJDXGB71s8fXCvH"
    lang = "en"
    resp = None
    error = None
 #   reCaptcha = recaptchalib.ReCaptcha(secret)
#    req.write('<p>'+ response.read() + '</p>')
    # Check for ReCaptcha Response
    #if util.get["g-recaptcha-response"]:
    #   resp = reCaptcha.verify_response(req.connection.remote_ip, util.get["g-recaptcha-response"])
#    if resp is not None and resp.success:
 #       req.write("<p>Good!</p>")
    req.write('<label for="text" class="sr-only">Username</label>')
    req.write('<input type="text" name="username" id="username" class="form-control" placeholder="Username" required autofocus>')
    req.write('<label for="inputEmail" class="sr-only">Email address</label>')
    req.write('<input type="inputEmail" name="email" id="inputEmail" class="form-control" placeholder="Email address" required>')
    req.write('<label for="inputPassword" class="sr-only">Password</label>')
    req.write('<input type="password" name="password1" id="inputPassword" class="form-control" placeholder="Password" required>')
    req.write('<label for="inputPassword" class="sr-only">Password</label>')
    req.write('<input type="password" name="password2" id="inputPassword" class="form-control" placeholder="Repeat Password" required>')
    req.write('<div name="g-recaptcha-response" class="g-recaptcha" data-sitekey="6LdT2gITAAAAAEnTL8_OaiIOli0I7H7-9MKhpanN" required></div>')
    req.write('<script type="text/javascript" src="https://www.google.com/recaptcha/api.js?hl=' + lang + '"></script>')
    req.write('<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>')
    req.write("</form></html>")

	
def register(req, username, email, password1, password2):

    session = Session.Session(req)
    
    if password1 == password2:
        user_password = mysql_password(password1)
    else:
        session['msg'] = 9
        session.save()    
        util.redirect(req, "/register")
    user_name = str(username).replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "").replace(",", "").replace("<", "").replace(">", "").replace("*", "").replace("(", "").replace(")", "").replace("/", "").replace("\\", "").replace(";", "").replace("{", "").replace("}", "")
    user_email = str(email).replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "").replace(",", "").replace("<", "").replace(">", "").replace("*", "").replace("(", "").replace(")", "").replace("/", "").replace("\\", "").replace(";", "").replace("{", "").replace("}", "")


    if '@' not in user_email:
        session['msg'] = 4
        session.save()
        util.redirect(req, "/register")

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

    #redirect if the user exists
    for thing in users:
        if user_name in thing:
            session['msg'] = 5
            session.save()
            util.redirect(req, "/register")
	
    #open a connection to the DB server
    curs = conn.cursor()
	
    #execute a check to see if
    curs.execute("INSERT INTO PS_Users (User_Name, User_Password, Total_Points, User_Email) VALUES (%s,%s,%s,%s)",(user_name, user_password, defualt_score, user_email ))
		
    #commit and close connection to database
    conn.commit()
    curs.close()

    #create session cookie with user name    
    session['login'] = user_name
    session['msg'] = 1
    session.save()
    util.redirect(req, "/")


