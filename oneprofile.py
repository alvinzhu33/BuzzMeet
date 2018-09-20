#!/usr/bin/python

import cgi,cgitb,os
cgitb.enable()

form = cgi.FieldStorage()
keys= form.keys()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>
<head>
<title>My Match's Profile</title>
<link rel="stylesheet" type="text/css" href="BuzzMeet.css">
</head>
<body>''' 

footer = '''</body>
</html>'''

def navigation():
    return '''<center><img src="../Pictures/logo.png" height = 70>
<ul id="menu">
<li>''' + makeLinkReg("home.py", "Home") + '''</li>
<li>''' + makeLinkReg("profile.py", "Profile") + '''</li>
<li>''' + makeLinkReg("quiz1.py", "Quiz Adventure") + '''</li>
<li>''' + makeLinkReg("match.py", "My Match") + '''</li>
<li>''' + makeLinkReg("logout.py", "Log Out") + '''</li>
</ul></center>
<br><br><br>'''

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

def keepaddress():
    if 'user' in form and 'magicnumber' in form and 'match' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        match = form.getvalue('match')
        return "?user="+user+"&magicnumber="+magicnumber+"&match=" + match
    return ""

def makeLink(page, text):
    return '<a href="'+ page + keepaddress()+'" id="clickables" style="background-color:#89b4fd;font-size:20px">'+text+'</a>'

def makeTable(s):
    text=s.split("\n")
    ans='''<table class="box">\n'''
    for line in text:
        line=line.split("|")
        ans+="<tr>"
        for i in line:
            ans+= "<td>"+i+"</td>"
        ans+="</tr>\n"
    return ans + "</table>"

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

def getquizinfo(L):
    ans="<strong style='font-size:25px'>Food Quiz Results </strong><br>"
    ans+="My favorite fastfood: <strong>" + L[1] + "</strong><br>"
    ans+="My favorite part of food pyramid: <strong>" + L[2] + "</strong><br>"
    ans+="My favorite country's food: <strong>" + L[3] + "</strong><br>"
    ans+="Where to eat: <strong>" + L[4] + "</strong><br>"
    ans+="How much I'm willing to spend on food: <strong>" + L[5] + "</strong><br><br>"
    ans+="<strong style='font-size:25px'>Entertainment Quiz Results </strong><br>"
    ans+="My favorite movie genre: <strong>" + L[6] + "</strong><br>"
    ans+="My favorite teenage girl movie: <strong>" + L[7] + "</strong><br>"
    ans+="My favorite type of music: <strong>" + L[8] + "</strong><br>"
    ans+="When I watch a movie: <strong>" + L[9] + "</strong><br>"
    ans+="My favorite show is: <strong>" + L[10] + "</strong><br><br>"
    ans+="<strong style='font-size:25px'>Lifestyle Quiz Results </strong><br>"
    ans+="How many children I want: <strong>" + L[11] + "</strong><br>"
    ans+="Dream city I want to live in: <strong>" + L[12] + "</strong><br>"
    ans+="What pet I want: <strong>" + L[13] + "</strong><br>"
    ans+="I exercise: <strong>" + L[14] + "</strong><br>"
    ans+="My dream job is: <strong>" + L[15] + "</strong><br>"
    return ans

def getinfo(L):
    ans = "<strong style='font-size:25px'>Personal Information</strong><br>"
    ans += "I am a: <strong>" + L[1] + "</strong><br>"
    ans += "My sexual orientation is: <strong>" + L[2] + "</strong><br>"
    ans += "I am: <strong>" + L[3] + "</strong> years old<br>"
    ans += "I live in: <strong>" + L[4] + ", " + L[5] + "</strong><br>"
    ans += "My email is: <strong>" + L[6] + "</strong><br>"
    return ans
    
def getUser(user):
    data = open("../profiles.txt","r").read().strip().split('\n')
    users = []
    for x in range(len(data)):
        users += [data[x].split(",")[0]]
    if user in users:
        return users.index(user)
    else:
        return "Error"

def profile(user):
    ans=""
    text = open("../profiles.txt","r").read().strip().split('\n')
    if getUser(user) != "Error":
        ans += getquizinfo(text[getUser(user)].strip(",").split(","))
    else:
        ans+= "This profile is quite empty! The user needs to go fill out our quizzes!"
    return ans

def getUserBasic(user):
    data = open("../info.txt","r").read().strip().split('\n')
    users = []
    for x in range(len(data)):
        users += [data[x].split(",")[0]]
    if user in users:
        return users.index(user)
    else:
        return "Error"
    
def profileBasic(user):
    ans=""
    text = open("../info.txt","r").read().strip().split('\n')
    if getUserBasic(user) != "Error":
        ans += getinfo(text[getUserBasic(user)].strip(",").split(","))
    else:
        ans+= "This profile is quite empty! The user needs to fill out their profile info!"
    return ans

def userlink(page, text):
    return '<a href="'+ page +'">'+text+'</a>'

def main():
    ans=""
    if authenticate():
        if 'match' in form:
            match = form.getvalue('match')
            ans = "<h2>Welcome to " + match + "'s Profile Page!</h2><br>"
            ans += makeTable(profileBasic(match))+ "<br><br>" + makeTable(profile(match))
    else:
        ans += notLoggedIn()
    return header + navigation() + ans + footer

print main()

