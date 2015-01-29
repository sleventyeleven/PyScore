PyScore
=======

A very Simple Python Based Scoring Engine

Currently works.

Features
========
Bootstrap Theme and CSS
Basic and Scalable 
MySQL Backend 
Session Based User Management

To Come:
========
Admin Page with:
    -Ability to manage users 
    -Ability to manage challenges 
Branding/Campaign Support 
An Actual Install Script

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
                PythonHandler mod_python.publisher
                PythonDebug On
                
        </Directory>
...


Your database structure should be something like the following.

--
-- Database: `PyScore`
--

-- --------------------------------------------------------

--
-- Table structure for table `PS_Challenges`
--

CREATE TABLE IF NOT EXISTS `PS_Challenges` (
  `Challenge_Completed` text NOT NULL,
  `Point_Value` int(11) NOT NULL,
  `Challenge_Text` text NOT NULL,
  `Challenge_Answer` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `PS_Users`
--

CREATE TABLE IF NOT EXISTS `PS_Users` (
  `User_Name` text NOT NULL,
  `User_Password` text NOT NULL,
  `Total_Points` int(11) NOT NULL,
  `User_Email` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

  
  
More detailed information to come.
