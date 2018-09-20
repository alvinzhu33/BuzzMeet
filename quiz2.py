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

quiz = '''<h3>Entertainment</h3>

<form method="GET" action="quiz2.py">

1. What is you favorite movie genre?
<table class="quiz">
<tr>
<td><input type="radio" name="b1" value="Comedy">Comedy </td> <td><img src="../Pictures/comedy.jpg" height=100></td>
<td><input type="radio" name="b1" value="Horror">Horror</td> <td><img src="../Pictures/horror.png" height=100><td>
</tr>
<tr>
<td><input type="radio" name="b1" value="Action">Action</td> <td> <img src="../Pictures/action.jpg" height=100></td>
<td><input type="radio" name="b1" value="Romance">Romance</td><td> <img src="../Pictures/romance.jpg" height=100></td>
</tr>
</table>
<br>

2. What is your favorite teenage girl movie?
<table class="quiz">
<tr>
<td><input type="radio" name="b2" value="Twilight">Twilight</td>  <td><img src="../Pictures/twilight.jpg" height=100></td>
<td><input type="radio" name="b2" value="The Hunger Games">The Hunger Games</td>  <td><img src="../Pictures/hungergames.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="b2" value="Mean Girls">Mean Girls</td> <td><img src="../Pictures/meangirls.gif" height=100></td>
<td><input type="radio" name="b2" value="Pitch Perfect">Pitch Perfect</td> <td><img src="../Pictures/pitchperfect.jpg" height=100></td>
</tr>
</table>
<br>

3. What is your favorite type of music?
<table class="quiz">
<tr>
<td><input type="radio" name="b3" value="Hip Hop">Hip Hop</td> <td><img src="../Pictures/hiphop.jpg" height=100></td>
<td><input type="radio" name="b3" value="Pop">Pop</td> <td><img src="../Pictures/pop.gif" height=100></td>
</tr>
<tr>
<td><input type="radio" name="b3" value="Rock">Rock</td> <td><img src="../Pictures/rock.jpg" height=100></td>
<td><input type="radio" name="b3" value="Classical">Classical</td> <td><img src="../Pictures/classical.jpg" height=100></td>
</tr>
</table>
<br>

4. When do you usually watch a new movie?
<table class="quiz">
<tr>
<td><input type="radio" name="b4" value="On opening weekend">On opening weekend</td> <td><img src="../Pictures/movies.jpg" height=100></td>
<td><input type="radio" name="b4" value="When it's on DVD">when it's on DVD</td> <td><img src="../Pictures/dvd.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="b4" value="When it's available online">When it's available online(if you know what I mean)</td> <td><img src="../Pictures/online.jpg" height=100></td>
<td><input type="radio" name="b4" value="Sometime in theatres">Sometime when it's in theatres</td> <td><img src="../Pictures/theater.jpg" height=100></td>
</tr>
</table>
<br>

5. What is your favorite TV Show?
<table class="quiz">
<tr>
<td><input type="radio" name="b5" value="Game of Thrones">Game of Thrones</td> <td><img src="../Pictures/gameofthrones.jpg" height=100></td>
<td><input type="radio" name="b5" value="Orange is the New Black">Orange is the New Black</td> <td><img src="../Pictures/oinb.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="b5" value="Once Upon a Time">Once Upon a Time</td> <td><img src="../Pictures/ouat.jpg" height=100></td>
<td><input type="radio" name="b5" value="The Big Bang Theory">The Big Bang Theory</td> <td><img src="../Pictures/bigbang.jpeg" height=100></td>
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
<input type="submit" name="b" value="Next">
</form>'''

def save(user, form, list):
    users = open("../profiles.txt","a")
    for x in list[1:6]:
        answer = form.getvalue(x)
        users.write(answer + ",")
    users.close()

def quizcompleted(user):
    users = open("../profiles.txt","r").read().strip().split("\n")
    listofusers = []
    for x in range(len(users)):
        listofusers += [users[x].split(",")[0]]
    if user in listofusers:
        return len(users[listofusers.index(user)].split(","))
    else:
        return "continue"

def main():
    form = cgi.FieldStorage()
    data = form.keys()
    data.sort()
    user = form.getvalue("user").strip("'")
    magicnum = form.getvalue("magicnumber").strip("'")
    ans = ""
    if authenticate():
	if quizcompleted(user) == 7 or quizcompleted(user) == "continue":
	    if len(data) < 8:
                ans+= quiz + hidden(user, magicnum)
            if len(data) == 8:
                save(user, form, data)
                ans+='<h2>DONE! Moving on to' + makeLink("quiz3.py","Lifestyle!") + '</h2>'
        else:
	    if quizcompleted(user) == 12:
    		    ans += '<h2>Now moving on to' + makeLink("quiz3.py","Lifestyle!") + '</h2>'
		    ans += str(data[1:6])
	    if quizcompleted(user) == 17:
		ans += '''Quizes already done! Would you like to start over?
<a href="clearprofile.py?user=''' + user + '&magicnumber=' + magicnum + '">Yes</a><center><a href="home.py?user=''' + user + '&magicnumber=' + magicnum + '">No</a>' 
    else:
        ans+= notLoggedIn()
    return header + navigation() + ans + footer
print main()
