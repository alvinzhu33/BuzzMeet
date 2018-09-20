#!/usr/bin/python
import cgi,cgitb,os,random,md5
cgitb.enable()

def header():
    return """content-type: text/html

<!DOCTYPE HTML>
<html>
<head>
<title>Create account</title>
<link rel="stylesheet" type="text/css" href="BuzzMeet.css">
</head>
<body>
"""

def footer():
    return """</body>
</html>"""

def md5Pass(password):
    m = md5.new()
    m.update(password)
    return m.hexdigest()

def checkIfNameExists(user):
    text = open('../user.txt').read().split("\n")
    for line in text:
        if line.split(",")[0] == user:
            return True
    return False

def valid(s):
    for c in s:
        if not (c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c >= '0' and c <= '9'):
            return False
    return True

def createAccount(form):
    result = ""
    if "name" in form and "user" in form and "pass" in form and "pass2" in form:
        name = form.getvalue("name")
        user = form.getvalue("user")
        password = form.getvalue("pass")
        password2 = form.getvalue("pass2")
        if checkIfNameExists(user):
            result += "Username <strong>"+ user +"</strong> already exists. Choose another. <a href='create.html'>Go back</a><br>"
        elif password != password2:
            result += "Passwords do not match! <a href='create.html'>Go back</a><br>"
        elif not valid(user) or not valid(name):
            result += "Username contains invalid characters. <a href='create.html'>Go back</a> <br>"
        else:
            result += "Account <strong>"+user+'</strong> created! Login here: <a href="login.html">login page</a><br>'
            f = open('../user.txt','a')
            password = md5Pass(password+user)
            f.write(user + "," + password + "," + name + "\n")
            f.close()
    else:
        result+="<h1>Please fill in all fields</h1>"
    return result


    
def notFilledIn():
    return '''You need to create an account using the form found <a href="create.html">here</a>\n'''

def main():
    form = cgi.FieldStorage()
    body = ""
    if len(form)==0:
        body += notFilledIn()
    else:
        body += createAccount(form)
    print header() + body + footer()
main()


