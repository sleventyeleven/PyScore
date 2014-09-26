from mod_python import apache
import MySQLdb
import hashlib

user_name = ""

def index(req):
    def __auth__(req, user, password):
        
        global user_name
        user_name = user
        pw = mysql_password(password)
	
        #check for null or none password
        if pw == "*BE1BDEC0AA74B4DCB079943E70528096CCA985F8":
            return 0
    
        #get the connection information for DB
        conn = Connect_To_Database()
    
        #open a connection to the DB server
        curs = conn.cursor()
	
        #clean user input
        user = user.replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "")
    
        #execute a check to see if
        curs.execute("SELECT User_Password FROM PS_Users WHERE User_Name =%s",(user))
    
	
        #catch the server response
        mysql_pw = curs.fetchone()
    
        #check for bad user
        if mysql_pw == None:
            curs.close()
            return 0
    
    
        if pw == mysql_pw[0]:
           curs.close()
           return 1
        else:
           curs.close()
           return 0    

    user = user_name
    challenges = Get_Challenges()
    req.content_type = "text/html"
    req.write('<link rel="stylesheet" href="../format.css" type="text/css" />')
    req.write("Logged in as: " + str(user))
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

    def __auth__(req, user, password):
       global user_name
       user_name = user
       pw = mysql_password(password)
       #check for null or none password
       if pw == "*BE1BDEC0AA74B4DCB079943E70528096CCA985F8":
           return 0
       #get the connection information for DB
       conn = Connect_To_Database()
       #open a connection to the DB server
       curs = conn.cursor()
       #clean user input
       user = user.replace('"', "").replace("'", "").replace("-", "").replace("+", "").replace("=", "")
       #execute a check to see if
       curs.execute("SELECT User_Password FROM PS_Users WHERE User_Name =%s",(user))
       #catch the server response
       mysql_pw = curs.fetchone()
       #check for bad user
       if mysql_pw == None:
            curs.close()
            return 0
       if pw == mysql_pw[0]:
            curs.close()
            return 1
       else:
            curs.close()
            return 0


    #get user
    user = user_name

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
		

def mysql_password(str):
    #This function is identical to the MySQL PASSWORD() function.
    pass1 = hashlib.sha1(str).digest()
    pass2 = hashlib.sha1(pass1).hexdigest()
    return "*" + pass2.upper()
