from mod_python import apache
import MySQLdb

def index(req):

    user = req.user
    challenges = Get_Challenges()
    req.content_type = "text/html"
    req.write('<link rel="stylesheet" href="format.css" type="text/css" />')
    req.write("Logged in as: " + user)
    req.write("<p>")
    req.write("Total Points: " + str(Get_Total_Points(user)).replace('L', ''))
    req.write("<p>")

    #reset counter and total
    counter = 0
    total = 0
    for challenge in challenges:

        #incrament counter and total
        counter += 1
        total += int(str(challenge[1]).replace('L', ''))

        #Display the challenge number and point value
        req.write("<p>")
        req.write("Challenge " + str(counter) + " worth " + str(challenge[1]).replace('L', '') + " points.")

        #indicate if the challenge has been complted
        if user in challenge[0].split(","):
            req.write("<p>")
            req.write("Status: Complete")

        else:
            req.write("<p><html>")
            req.write("Status: Open ")
            req.write('<form action="page.py/challenge" method="POST">')
            req.write('<input type="text" name="answer"><br>')
            req.write('<input type="hidden" name="challengenum" value="' + str(counter) + '">')
            req.write('<input type="submit">')
            req.write("</form></html>")

        #display the challenge text
        req.write("<p>" + str(challenge[2]))

    #indicate the end of challenges
    req.write("<p>End of Challenges <p>")
    req.write(str(counter) + " total challenges worth " + str(total) + " points.")

    return apache.OK

def Connect_To_Database():
    #connect to the Database
    conn = MySQLdb.connect(host="localhost", user="PyScore", passwd="P@ssw0rd", db="PyScore")
    #return the connection settings
    return conn

def Get_Total_Points(user):

    #get the connection information for DB
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
    return total_points[0]

def Get_Challenges():

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

    return ans

def challenge(req, answer, challengenum):

    #get user
    user = req.user

    #set content type to html
    req.content_type = "text/html"

    #get a list of the challenges
    challenges = Get_Challenges()

    if user in challenges[int(challengenum) - 1][0].split(","):
        return '<meta http-equiv="refresh" content="0;url=/">'

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
        return '<meta http-equiv="refresh" content="0;url=/">'
