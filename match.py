#!/usr/bin/python

import cgi,cgitb,os
cgitb.enable()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>

<head>
<title>Profile</title>
<link rel="stylesheet" type="text/css" href="BuzzMeet.css">
</head>

<body>
''' 

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

<h1>Find out who is perfect for you here!</h1><br>'''

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

footer = '''</body>
</html>'''

form = cgi.FieldStorage()
keys = form.keys()

def keepaddress():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber+"&match=" + match(user)
    return ""

def makeLink(page, text):
    return '<a href="'+ page + keepaddress()+'" id="clickables" style="background-color:#89b4fd;font-size:20px">'+text+'</a>'

def authenticate():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        IP = ""
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        text = open('../loggedin.txt').read().split("\n")
        for line in text:
            line = line.split(",")
            if line[0]==user:
                if line[1]==magicnumber and line[2]==IP:
                    return True
                else:
                    return False
        return False
    return False 

def notLoggedIn():
    return '''Sorry! You need to login to visit this page. You may do so <a href="login.html">here</a>!\n'''

def getUser(user):
    data = open("../profiles.txt","r").read().strip().split('\n')
    users = []
    for x in range(len(data)):
        users += [data[x].split(",")[0]]
    if user in users:
        return users.index(user)
    else:
        return 0

def quizcompleted(user):
    users = open("../profiles.txt","r").read().strip().split("\n")
    listofusers = []
    for x in range(len(users)):
        listofusers += [users[x].split(",")[0]]
    if user in listofusers:
        return "Done"

def match(user):
    users = open("../profiles.txt","r").read().strip().split("\n")
    person = 0
    counter = 0
    for x in range(len(users)):
        newcount = 0
        if x != getUser(user):
            for y in range(len(users[x].split(",")))[1:]:
                if users[x].split(",")[y] == users[getUser(user)].split(",")[y]:
                    newcount += 1
            if newcount > counter:
                person = x
                counter = newcount
    return users[person].split(",")[0]
            
def lover(name):
    return "<h2>Your potential lover is: " + name + "</h2> <br>"

def main():
    data = cgi.FieldStorage()
    user = data.getvalue("user")
    magicnum = data.getvalue("magicnumber")
    ans=""
    if authenticate():
        if quizcompleted(user) != "Done":
            ans += "You haven't gone on the Quiz Adventure yet! Start your Quiz Adventure <a href='quiz1.py?user=" + user + '&magicnumber=' + magicnum + "'>now</a>"
        else: 
            ans += lover(match(user)) + makeLink("oneprofile.py","Check out your potential lover's profile now!")
    else:
        ans += notLoggedIn()
    return header + navigation() + ans + footer
print main()
