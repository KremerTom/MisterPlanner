from google.appengine.ext import db

import datetime
import webapp2


class User(db.Model):
    email = db.StringProperty(required=True)

def createUser(emailAddress):
    user = User(email = emailAddress)
    q = User.all()
    q.filter("email =", emailAddress)

    if q.get() is None:
        user.put()
        print "successfully wrote " + emailAddress
        return True
    else:
        print emailAddress + " already exists"
        return False

class CreateUserWithParams(webapp2.RequestHandler):
    def post(self):
        email=self.request.get("email")
        self.response.out.write('<li>' + email + '</li>')

        if createUser(email):
            self.response.write("success")
        else:
            self.response.write("user already exists")

# create a new user with email set to "email" URL param
class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="post" action="/createuserwithparams">
                Enter Email Address:<br>
                <div><input type="text" name="email"></div>
                <div><input type="submit" value="Create Account"></div>
              </form>""")

# list all users
class ListUsers(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        #write all users in system
        q = User.all()
        for p in q.run():
            self.response.write("<li>Email: " + p.email + ", ID: " + str(p.key().id()) + "</li>\n")


usersPages = [('/createuser', CreateUser), ('/createuserwithparams', CreateUserWithParams), ('/listusers', ListUsers)]
