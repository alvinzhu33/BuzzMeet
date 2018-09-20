#!/usr/bin/python

import cgi,cgitb, os
cgitb.enable()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>

<head>
<title>Profile Information</title>
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
</ul>
<br><br><br>

<center><img src="../Pictures/logo.png" height = 70></center><br><br><br>
'''

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

quiz = '''<h3>Profile information</h3>
<h5>Please review all your answers because you will not be able to change them</h5>

<form method="GET" action="profileinfo.py">

1. Which gender do you identify with?

<select name="d1" size="1">
<option>Male</option>
<option>Female</option>
<option>Neither</option>
<option>Don't want to say</option>
</select>
<br>

2. What is you sexual orientation?

<select name="d2" size="1">
<option>Straight</option>
<option>Gay/Lesbian</option>
<option>Bisexual</option>
<option>Asexual</option>
<option>Don't want to say</option>
</select>
<br>

3. How old are you?

<input type="text" name="d3" size="2">
</input>
<br>

4. Which city do you live in?

<input type="text" name="d4" size="20">
</input>
<br>

5. Which country do you live in?

<input type="text" name="d5" size="20">
</input>
<br>

6. What is your email address?

<input type="text" name="d6" size="50">
</input>
<br>'''

footer = '''</body>
</html>'''

form = cgi.FieldStorage()
keys = form.keys()

def keepaddress():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
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

def hidden(user, magicnum):
    return '<input type="hidden" name="user" value = "' + user + '''">
<input type="hidden" name="magicnumber" value="''' + magicnum + '''">
<input type="submit" name="d" value="Done">
</form>'''

def save(user, form, list):
    users = open("../info.txt","a")
    text = open("../info.txt","r")
    if not user in text:
        users.write(user + ",")
        for x in list[1:7]:
            answer = form.getvalue(x)
            users.write(answer + ",")
    users.write("\n")
    text.close()    
    users.close()

def quizcompleted(user):
    users = open("../info.txt","r").read().strip().split("\n")
    listofusers = []
    for x in range(len(users)):
        listofusers += [users[x].split(",")[0]]
    if user not in listofusers:
        return "continue"

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

def main():
    form = cgi.FieldStorage()
    data = form.keys()
    data.sort()
    user = form.getvalue("user").strip("'")
    magicnum = form.getvalue("magicnumber")
    ans=""
    if authenticate():
        if quizcompleted(user) != "continue":
            ans += '<h2>Profile information already set! Back to your' + makeLink("profile.py","Profile Page") +'</h2>'
        else:
            if len(data) < 9:
                ans += quiz + hidden(user, magicnum)
            if len(data) == 9:
                save(user, form, data)
                ans += '<h2>DONE! Back to your' + makeLink("profile.py","Profile Page") +'</h2>'
    else:
        ans += notLoggedIn()
    return header + navigation() + ans + footer
print main()
