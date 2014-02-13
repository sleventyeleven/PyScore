from mod_python import apache
import MySQLdb

def handler(req):

    user = req.user
    challenges = Get_Challenges()
    req.content_type = "text/plain"
    req.write("\nLoged in as: " + user)
    req.write("\nTotal Points: " + str(Get_Total_Points(user)).replace('L', ''))
    req.write("\n")
	
	  #reset counter and total
    counter = 0
    total = 0
    for challenge in challenges:
        
        #incrament counter and total
        counter += 1
        total += int(str(challenge[1]).replace('L', ''))
		
        #Display the challenge number and point value
        req.write("\n\nChallenge " + str(counter) + " worth " + str(challenge[1]).replace('L', '') + " points.")
		
        #indicate if the challenge has been complted
        if user in challenge[0].split(","):
            req.write("\nStatus: Complete\n")
        
        else:
            req.write("\nStatus: Open\n")
		
        #display the challenge text
        req.write("\n" + str(challenge[2]))
    
    #indicate the end of challenges
    req.write("\n\n\nEnd of Challenges \n" + str(counter) + " total challenges worth " + str(total) + " points.")
	
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
    curs.execute("SELECT Total_Points FROM PS_Users WHERE User_Name =%s",(user))
    
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
