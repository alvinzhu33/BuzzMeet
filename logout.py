#!/usr/bin/python
import cgi,cgitb,os
cgitb.enable()

form = cgi.FieldStorage()
keys= form.keys()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>

<head>
<title>Logout</title>
<link rel="stylesheet" type="text/css" href="BuzzMeet.css">
</head>

<body>
<h1 id="logo"><center>Buzz&Meet</center></h1>
<h2>You are here because you want to log out!</h2><br>
Attempting to log you out...''' 

footer = '''</body>
</html>'''

def remove(user,magicnumber):
    text = open('../loggedin.txt','r').read()
    result = "User not logged out<br>\n"
    if (user+",") in text:
        outfile = open('../loggedin.txt','w')
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i]=lines[i].split(",")
            if len(lines[i]) > 2:
                if(lines[i][0] != user or lines[i][1] != str(magicnumber) ):
                    outfile.write(','.join(lines[i])+"\n")
                else:
                    result = "Logout successful!<br>\n"
        outfile.close();
    else:
        result = "User not found<br>\n"
    return result


def processForm(form):
    if( 'user' in form and 'magicnumber' in form):
        user = form.getvalue('user')
        mn = form.getvalue('magicnumber')
        return remove(user,mn)
    return "You must be logged in properly to log out!<br>\n"

def notLoggedIn():
    return "You must be loggedin before trying to log out!<br>\n"

def returnlink():
    return '<h3>Click here to <a href="login.html"> log back in! </a></h3>'

def main():
    form = cgi.FieldStorage()
    body = ""
    if len(form)==0:
        body += notLoggedIn()
    else:
        body += processForm(form) + returnlink()
    return header + body + footer

print main()
