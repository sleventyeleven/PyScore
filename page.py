from mod_python import Session, apache, util
from lib import *

def index(req):

    session = Session.Session(req)
    try:
        user_name = session['login']

    except:
        user_name = ""

    challenges = Get_Challenges()
    Print_Header(req)

    if user_name == "":
        req.write("<center><h2>Login to submit flags</h2></center>")

    req.write('<link rel="stylesheet" href="/css/login.css">')
    req.write('<div class="container">')

    #reset counter and total
    counter = 0
    total = 0
    for challenge in challenges:

        #incrament counter and total
        counter += 1
        total += int(str(challenge[1]).replace('L', ''))
        
        #Display the challenge number and point value
        req.write("<p>")
        req.write("<center><h4>Challenge " + str(counter) + " worth " + str(challenge[1]).replace('L', '') + " points.</h4></center>")

        #indicate if the challenge has been complted 
        if user_name == "":
           req.write("")

        elif user_name in challenge[0].split(","):
            req.write("<p>")
            req.write("<center>Status: Complete</center>")

        else:
            req.write("<p><html>")
            req.write("<center><h3> Status: Open </h3></center>")
            req.write('<form class="form-signin" action="page.py/challenge" method="POST">')
            req.write('<input type="text" name="answer" class="form-control" placeholder="Answer"><br>')
            req.write('<input type="hidden" name="challengenum" value="' + str(counter) + '">') 
            req.write('<button class="btn btn-primary btn-block" type="submit">Submit</button>')
            req.write("</form></html>")

        #display the challenge text
        req.write("<center><p>" + str(challenge[2]) + "</center>")

    #indicate the end of challenges
    req.write("<center><h2>End of Challenges</h2></center>")
    req.write("<center><h3>" + str(counter) + " total challenges worth " + str(total) + " points.<h/3></center>")

    return apache.OK

def challenge(req, answer, challengenum):

    session = Session.Session(req)
    try:
        user = session['login']

    except:
        util.redirect(req, "/login")


    #set content type to html
    req.content_type = "text/html"

    #get a list of the challenges
    challenges = Get_Challenges()

    if user in challenges[int(challengenum) - 1][0].split(","):
        util.redirect(req, "/")

    if challenges[int(challengenum) - 1][3] == answer:

        #get the connection information for DB
        conn = Connect_To_Database()

        #open a connection to the DB server
        curs = conn.cursor()

        userlist = challenges[int(challengenum) - 1][0] + "," + user
        #add the user to the completed challenge list
        curs.execute("UPDATE PS_Challenges SET Challenge_Completed=%s WHERE Challenge_Answer=%s", (userlist, answer))

        #update the total points earned
        total = int(Get_Total_Points(user)) + int(challenges[int(challengenum) - 1][1])
        curs.execute("UPDATE PS_Users SET Total_Points =%s WHERE User_Name =%s", (str(total), user))

        #commit and close connection to database
        conn.commit()
        curs.close()
        util.redirect(req, "/")

    else:
        util.redirect(req, "/")		
