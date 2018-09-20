#!/usr/bin/python
import cgi,cgitb,os
cgitb.enable()

form = cgi.FieldStorage()
keys= form.keys()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>
<head>
<title>Homepage</title>
<link rel="stylesheet" type="text/css" href="BuzzMeet.css">
</head>
<body>''' 

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


<h1> Welcome to <span id="logo">Buzz&Meet</span>! </h1><br>'''

def keepaddress():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
    return ""

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

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

def homepage():
    return '''<p>Here at <span id="logo" style="font-size:20px">Buzz&Meet</span>, we are dedicated to finding <strong>your</strong> Mr./Mrs. Perfect!<br>
But for us to help you, you must help us first by taking quizzes so we (and your potential love) can get to know you better!<br>
This will build your profile and allow others to view your interests/hobbies!<br>
When you finish all the quizzes, we will match you up with someone who may be a <strong>perfect</strong> fit for you!<br>
Have fun and start mingling!</p>'''

def quizcenter():
    form = cgi.FieldStorage()
    user = form.getvalue("user")
    magicnum = form.getvalue("magicnumber")
    return '<center><a href="quiz1.py?user=' + user + '&magicnumber=' + magicnum + '''" id="clickables" style="background-color:#f55b5b;font-size:20px">Start Your Quiz Adventure</a></center>'''

def match():
    form = cgi.FieldStorage()
    user = form.getvalue("user")
    magicnum = form.getvalue("magicnumber")
    return '<center><a href="match.py?user=' + user + '&magicnumber=' + magicnum + '''" id="clickables" style="background-color:pink;font-size:20px">Match</a></center>'''

def getPics():
    return '''<br><br><h3>Look at all the happy couples <span id="logo">Buzz&Meet</span> helped to create</h3>
<center>
<table>
<tr><th>Romeo and Juliet</th><th>Tyrion and Sansa</th><th>Kim and Kris</th><th>Paris and Helen</th></tr>
<tr><td><img src="../Pictures/romeojuliet.jpg" height=200></td><td><img src="../Pictures/Tyrion and Sansa.png" height=200></td><td><img src="../Pictures/kimandkris.jpg" height=200></td><td><img src="../Pictures/ParisHelen.jpg" height=200></td></tr>
</table>
</center>
<h3>Trust us, this really works!</h3>'''

def home():
    ans=""
    if authenticate():
        ans+= makeTable(homepage()) + getPics() + "<br>"
    else:
        ans+= notLoggedIn()
    return header + navigation() + ans + footer
print home()
