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
''' 

footer = '''</body>
</html>'''

def navigation():
    return '''<ul id="menu">
<li>''' + makeLinkReg("home.py", "Home") + '''</li>
<li>''' + makeLinkReg("profile.py", "Profile") + '''</li>
<li>''' + makeLinkReg("quiz1.py", "Quiz Adventure") + '''</li>
<li>''' + makeLinkReg("match.py", "My Match") + '''</li>
<li>''' + makeLinkReg("logout.py", "Log Out") + '''</li>
</ul>
<br><br><br>

<center><img src="../Pictures/logo.png" height = 70></center>

<h1>Profile Cleared!</h1><br>'''

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

def remove(user):
    text = open('../profiles.txt','r').read()
    result = "User not logged out<br>\n"
    if (user + ",") in text:
        outfile = open('../profiles.txt','w')
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i]=lines[i].split(",")
            if len(lines[i]) > 2:
                if lines[i][0] != user:
                    outfile.write(','.join(lines[i])+"\n")
                else:
                    result = "Profile cleared!<br>\n"
        outfile.close()
    else:
        result = "Your profile has been cleared!<br>\n"
    return result


def processForm(form):
    if( 'user' in form and 'magicnumber' in form):
        user = form.getvalue('user')
        return remove(user)
    return "You must be logged in properly to log out!<br>\n"

def notLoggedIn():
    return "You must be logged in before clearing your profile!<br>\n"

def returnlink():
    return '<h3>Restart your <a href="quiz1.py?user=' + form.getvalue('user') + '&magicnumber=' + form.getvalue('magicnumber') + '">Quiz Adventure</a></h3>'

def main():
    body = ""
    if len(form)==0:
        body += notLoggedIn()
    else:
        body += processForm(form) + returnlink()
    return header + navigation() + body + footer

print main()
