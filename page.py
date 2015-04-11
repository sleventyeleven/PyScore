from mod_python import apache, Session
from lib import *

def index(req):

    session = Print_Header(req)
    Get_Challenges(session)
    try:
        user_name = session['login']

    except:
        user_name = ""
    challenges = session['challenges']
 
    if user_name == "":
         req.write("<center><h2>Login to submit flags</h2></center>")

    req.write('<link rel="stylesheet" href="/css/login.css">')
    req.write('<div class="container">')

    req.write("<p><br>")
    req.write("<center><h2>Challenges</h2></center>")
    req.write('<div class="col-sm-4">')
    req.write('<table class="table">')
    req.write('<thead>')
    req.write('<tr>')
    req.write('<th>#</th>')
    req.write('<th>Status</th>')
    req.write('<th>Value</th>')
    req.write('<th>Challenge Text</th>')
    req.write('</tr>')
    req.write('</thead>')
    req.write('<tbody>')


    counter = 0
    total = 0
    for challenge in challenges:
         counter += 1
         total += int(str(challenge[1]).replace('L', ''))

         req.write('<tr>')
         req.write('<td>' + str(counter) + '</td>')
         if user_name == "":
             req.write('<td> Login </td>')
         elif user_name in challenge[0].split(","):
             req.write('<td> Complete </td>')
         else:
             req.write('<td> Open </td>')
         req.write('<td>' + str(challenge[1]).replace('L', '') + '</td>')
         req.write('<td><div style="width: 650px; height: 80px;  text-align: left; white-space: nowrap; overflow:hidden;">' + str(challenge[2]) + '</div></td>')

         if user_name not in challenge[0].split(","):
             req.write('<form class="form-signin" action="page.py/challenge" method="POST">')
             req.write('<td><div style="width: 150px; height: 15px;"><input type="text" name="answer" class="form-control" placeholder="Answer"><br></div></td>')
             req.write('<td><input type="hidden" name="challengenum" value="' + str(counter) + '"></td>')
             req.write('<td><div style="width: 80px; height: 15px;"><button class="btn btn-primary btn-block" type="submit">Submit</button></td>')
             req.write("</form>")


    req.write('</tr>')
    req.write('</center></tbody>')
    req.write('</table>')
    req.write('</div>')
    req.write('<div style="position: fixed; bottom: 0; left: 0px; background-color: #f5f5f5; border: 1px solid LightGray; border-radius: 3px; padding: 3px; padding-bottom: 0px;">')
    req.write("<center><h5>" + str(counter) + " total challenges worth " + str(total) + " points.</h5></center>")
    req.write('</div>')

def challenge(req, answer, challengenum):

     session = Session.Session(req)
     try:
          user = session['login']

     except:
          util.redirect(req, "/login")


     #set content type to html
     req.content_type = "text/html"

     #get a list of the challenges
     Get_Challenges(session)
     challenges = session['challenges']

     if user in challenges[int(challengenum) - 1][0].split(","):
          session['msg'] = 8
          session.save()
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
          total = int(Get_Total_Points(session)) + int(challenges[int(challengenum) - 1][1])
          curs.execute("UPDATE PS_Users SET Total_Points =%s WHERE User_Name =%s", (str(total), user))

          #commit and close connection to database
          conn.commit()
          curs.close()
          util.redirect(req, "/")

     else:
          session['msg'] = 7
          session.save()
          util.redirect(req, "/")
