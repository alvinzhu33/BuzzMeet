#!/usr/bin/python

import cgi,cgitb, os
cgitb.enable()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>

<head>
<title>Food Quiz</title>
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

quiz = '''<h3>Food</h3>

<form method="GET" action="quiz1.py">

1. What is your favorite fast food?
<table class="quiz">
<tr>
<td><input type="radio" name="a1" value="McDonald's">McDonalds</td><td><img src="../Pictures/food1-1.png" height=100></td>
<td><input type="radio" name="a1" value="Burger King">Burger Kings</td><td><img src="../Pictures/food1-2.png" height=100></td>
</tr>
<tr>
<td><input type="radio" name="a1" value="Subway">Subway</td><td><img src="../Pictures/food1-3.png" width=200></td>
<td><input type="radio" name="a1" value="Dunkin' Donuts">Dunkin Donuts</td><td><img src="../Pictures/food1-4.png" height=100></td>
</tr>
</table>
<br>

2. What is your favorite part of the food pyramid?
<table class="quiz">
<tr><td><input type="radio" name="a2" value="Grains">Grains<br>
<input type="radio" name="a2" value="Vegetables">Vegetables<br>
<input type="radio" name="a2" value="Proteins">Proteins<br>
<input type="radio" name="a2" value="Dairy">Dairy<br></td>
<td><img src="../Pictures/pyramid.jpg" height=175></td>
</tr>
</table>
<br>

3. Which country's food do you like the most?
<table class="quiz">
<tr>
<td><input type="radio" name="a3" value="China">China</td><td><img src="../Pictures/tofu.jpg" height=100></td>
<td><input type="radio" name="a3" value="Italy">Italy</td><td><img src="../Pictures/pasta.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="a3" value="India">India</td><td><img src="../Pictures/indian.jpg" height=100></td>
<td><input type="radio" name="a3" value="Mexico">Mexico</td><td><img src="../Pictures/taco.jpg" height=100></td>
</tr>
</table>
<br>

4. Where would you perfer to eat?
<table class="quiz">
<tr>
<td><input type="radio" name="a4" value="Fancy 5-star restaurant">Fancy 5-star restaurant</td><td><img src="../Pictures/5star.jpg" height=100></td>
<td><input type="radio" name="a4" value="Fast Food Restaurants">Fast food restaurant</td><td><img src="../Pictures/fastfood.jpg" height=100></td>
</tr>
<tr>
<td><input type="radio" name="a4" value="Hipster Cafes/Restaurants">Hipster cafes/brunches</td><td><img src="../Pictures/cafe.jpg" height=100></td>
<td><input type="radio" name="a4" value="At home">At home</td><td><img src="../Pictures/home.jpg" height=100></td>
</tr>
</table>
<br>

5. How much are you willing to spend on dinner?
<table class="quiz">
<tr>
<td><input type="radio" name="a5" value="$10">$10<br>
<input type="radio" name="a5" value="$20">$20<br>
<input type="radio" name="a5" value="$50">$50<br>
<input type="radio" name="a5" value="$100+">$100+</td>
<td><img src="../Pictures/money.png" height=100></td>
</tr>
</table><br>'''

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
<input type="submit" name="a" value="Next">
</form>'''

def save(user, form, list):
    users = open("../profiles.txt","a")
    text = open("../profiles.txt","r")
    if not user in text:
        users.write(user + ",")
        for x in list[1:6]:
            answer = form.getvalue(x)
            users.write(answer + ",")
    text.close()    
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
            if quizcompleted(user) < 10:
                ans += '<h2>Now moving on to' + makeLink("quiz2.py","Entertainment") +'</h2>'
	    if quizcompleted(user) < 15 and quizcompleted(user) > 10:
		ans += '<h2>Now moving on to' + makeLink("quiz3.py","Lifestyle") +'</h2>'
            if quizcompleted(user) == 17:
                ans += '''<center>Quizes already done! Would you like to start over?'''+makeTable('''<a href="clearprofile.py?user=''' + user + '&magicnumber=' + magicnum + '''">Yes</a>
<a href="home.py?user=''' + user + '&magicnumber=' + magicnum + '">No</a></center>')
        else:
            if len(data) < 8:
                ans += quiz + hidden(user, magicnum)
            if len(data) == 8:
                save(user, form, data)
                ans += '<h2>DONE! Now moving on to' + makeLink("quiz2.py","Entertainment") +'</h2>'
    else:
        ans += notLoggedIn()
    return header + navigation() + ans + footer
    
print main()
