PyScore
=======

A very Simple Python Based Scoring Engine

Currently In the works.

Requires
========

python 2.5+
Python MySQLdb
MySQL 5.0+
Apache 2.2+
mod_python



Installation
============

In order for the side to work, mod_python must be installed and your apache configure should look something like this.


...        
        <Directory /var/www/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
                DirectoryIndex page.py
                AuthBasicAuthoritative off
                AddHandler mod_python .py
                PythonHandler page
                PythonDebug On
                PythonAuthenHandler auth
                AuthType Basic
                AuthName "Restricted Area"
                require valid-user
        </Directory>
...


Your database structure should be something like the following.


PyScore
  PS_Users: User_Name 	User_Password 	Total_Points
  PS_Challenges: Challenge_Completed 	Point_Value 	Challenge_Text 	Challenge_Answer
  
  
More detailed information to come.
