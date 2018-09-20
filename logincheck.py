#!/usr/bin/python
import random
import cgi,cgitb,os
cgitb.enable()
import md5

#Yvonne Chan & Alvin Zhu
#Period 1

form = cgi.FieldStorage()
keys= form.keys()

header = '''content-type: text/html

<!DOCTYPE HTML>
<html>
<head>
<title>Login Checker</title>
</head>
<body>''' 

footer = '''</body>
</html>'''

def md5Pass(password):
    m = md5.new()
    m.update(password)
    return m.hexdigest()

##def checkIfNameExists(user):
##    text = open('user.txt',"r").readlines()
##    for line in text:
##        if line.split(",")[0]==user:
##            return True
##    return False

def authenticate(user,password):
    password = md5Pass(password+user)
    text = open('../user.txt','r').readlines()
    for line in text:
        line = line.strip().split(",")
        if line[0]==user:
            if line[1]==password:
                return True
            else:
                return False

#remove a user, only do this if they successfully authenticated
#since this does not check to see if you have the right person
def remove(user):
    infile = open('../loggedin.txt','r')
    text = infile.read()
    infile.close()
    if (user+",") in text:
        outfile = open('../loggedin.txt','w')
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i]=lines[i].split(",")
            if len(lines[i]) > 1:
                if(lines[i][0] != user):
                    outfile.write(','.join(lines[i])+'\n')
        outfile.close()


#only meant to be run after password authentication passes.
#uses call to remove(user) that will remove them no matter what.
def logInUser(username):
    magicNumber = str(random.randint(10000000,99999999))
    remove(username)
    outfile = open('../loggedin.txt','a')
    IP = ""
    if "REMOTE_ADDR" in os.environ :
        IP = os.environ["REMOTE_ADDR"]
    outfile.write(username+","+magicNumber+","+IP+"\n")
    outfile.close()
    return magicNumber
            
def process(form):
    result = ""
    if not ('user' in form and 'pass' in form):
        return "Username or password not provided"
    user = form.getvalue('user')
    password = form.getvalue('pass')
    if authenticate(user,password):
        result += "Success!<br>\n"
        magicNumber = logInUser(user)
        result += '<a href="home.py?user='+user+'&magicnumber='+str(magicNumber)+'">Click here to go to meet your future!</a>'
    else:
        result += "Unable to log in, authentication failure"
    return result


def notLoggedIn():
    return '''<h1>Sorry! You need to login <a href="login.html">here</a> first before you can meet the love of your life!</h1>\n'''

def main():
    body = ""
    if len(form)==0:
        body += notLoggedIn()
    else:
        body += process(form)
    return header + body + footer

print main()
