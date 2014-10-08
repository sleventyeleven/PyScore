from mod_python import apache
import lib

def index(req):
#start registration process

    Print_Header(req)

    req.write('<form action="register.py/register" method="POST">')
    req.write("Do not lose this information!")
    req.write("<p>THERE IS NO METHOD OF RECOVERY!!!!")
    req.write("<p>Enter Username")
    req.write('<input type="text" name="name"><br>')
    req.write("<p>Enter Password")
    req.write('<input type="text" name="password"><br>')
    req.write('<input type="submit">')
    req.write("</form></html>")

	
def register(req, name, password):

    user_password = mysql_password(password)
	
    user_name = name
	
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
        return '<meta http-equiv="refresh" content="0;url=/register.py">'
	
    else:
	#open a connection to the DB server
        curs = conn.cursor()
	
	#execute a check to see if
        curs.execute("INSERT INTO PS_Users (User_Name, User_Password, Total_Points) VALUES (%s,%s,%s)",(user_name, user_password, defualt_score))
		
        #commit and close connection to database
        conn.commit()
        curs.close()
        return '<meta http-equiv="refresh" content="0;url=/">'
