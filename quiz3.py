#!/usr/bin/python

import cgi, cgitb, os
cgitb.enable()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>

<head>
<title>Entertainment Quiz</title>
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
</ul>
<br><br><br>

<center><img src="../Pictures/logo.png" height = 70></center><br><br><br>
'''

def makeLinkReg(page, text):
    return '<a href="'+ page + keepaddress()+'">'+text+'</a>'

quiz = '''<h3>Lifestyle</h3>

<form method="GET" action="quiz3.py">

1. How many children would you want?
<table class="quiz">
<tr>
<td><input type="radio" name="c1" value="1">1 <br>
<input type="radio" name="c1" value="2">2<br>
<input type="radio" name="c1" value="3">3<br>
<input type="radio" name="c1" value="4">4</td>
<td><img src="../Pictures/baby.jpg" height=150></td>
</tr>
</table>
<br>

2. Which big city would you live in?
<table class="quiz">
<tr>
<td><input type="radio" name="c2" value="New York City">New York City</td> <td><img src="../Pictures/nyc.jpg" height=100></td>
<td><input type="radio" name="c2" value="Chicago">Chicago</td><td><img src="../Pictures/chicago.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="c2" value="Los Angeles">Los Angeles</td> <td><img src="../Pictures/LA.jpg" height=100></td>
<td><input type="radio" name="c2" value="Seattle">Seattle</td> <td><img src="../Pictures/seattle.jpg" height=100></td>
</tr>
</table>
<br>

3. What pet do you want?
<table class="quiz">
<tr>
<td><input type="radio" name="c3" value="Dog">Dog</td> <td><img src="../Pictures/dogs.jpg" height=100></td>
<td><input type="radio" name="c3" value="Cat">Cat</td> <td><img src="../Pictures/cat.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="c3" value="Rabbit">Rabbit</td><td><img src="../Pictures/rabbit.jpg" height=100></td>
<td><input type="radio" name="c3" value="None">No pet</td><td><img src="../Pictures/alone.png" height=100></td>
</tr>
</table>
<br>

4. How much do you exercise per week?
<table class="quiz">
<tr>
<td><input type="radio" name="c4" value="Close to none">Close to none<br>
<input type="radio" name="c4" value="3-7 hours">3-7 hours<br>
<input type="radio" name="c4" value="8-14 hours">8-14 hours<br>
<input type="radio" name="c4" value="15+ hours">15+ hours</td>
<td><img src="../Pictures/exercise.gif" height=150></td>
</tr>
</table>
<br>

5. What is your dream job?
<table class="quiz">
<tr>
<td><input type="radio" name="c5" value="Doctor">Doctor</td><td><img src="../Pictures/doctor.jpg" height=100></td>
<td><input type="radio" name="c5" value="President">The President</td><td><img src="../Pictures/president.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="c5" value="Actor">Actor</td><td><img src="../Pictures/millionare.jpg" height=100></td>
<td><input type="radio" name="c5" value="Writer">Writer</td><td><img src="../Pictures/writer.jpg" height=100></td>
</tr>
</table>
<br>
'''
form = cgi.FieldStorage()
keys = form.keys()

def keepaddress():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
    return ""

def makeLink(page, text):
    return '<a href="'+ page + keepaddress()+'" id="clickables" style="background-color:#89c4fd;font-size:20px">'+text+'</a>'

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
<input type="submit" name="b" value="Next">
</form>'''

def save(user, form, list):
    users = open("../profiles.txt","a")
    for x in list[1:6]:
        answer = form.getvalue(x)
        users.write(answer + ",")
    users.write("\n")
    users.close()
        
def main():
    form = cgi.FieldStorage()
    data = form.keys()
    data.sort()
    user = form.getvalue("user").strip("'")
    magicnum = form.getvalue("magicnumber").strip("'")
    ans = ""
    if authenticate():
        if len(data) < 8:
            ans+= quiz + hidden(user, magicnum)
        if len(data) == 8:
            save(user, form, data)
            ans+='<h2>FINISHED! Go back to home and view your profile!</h2>'
    else:
        ans+= notLoggedIn()
    return header + navigation() + ans + footer
print main()
