from google.appengine.ext import db

import datetime
import webapp2


class User(db.Model):
    phoneNumber = db.PhoneNumberProperty(required=True)

def createUser(phone):
    user = User(phoneNumber = phone)
    q = User.all()
    q.filter("phoneNumber =", phone)

    if q.get() is None:
        user.put()
        print "successfully wrote " + phone
        return True
    else:
        print phone + " already exists"
        return False

class CreateUserWithParams(webapp2.RequestHandler):
    def post(self):
        phone=self.request.get("phone")
        self.response.out.write('<li>' + phone + '</li>')

        if createUser(phone):
            self.response.write("success")
        else:
            self.response.write("user already exists")

# create a new user with phone set to "phone" URL param
class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="post" action="/createuserwithparams">
                Enter phone number:<br>
                <div><input type="text" name="phone"></div>
                <div><input type="submit" value="Create Account"></div>
              </form>""")

# list all users
class ListUsers(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        #write all users in system
        q = User.all()
        for p in q.run():
            self.response.write("<li>Phone: " + p.phoneNumber + ", ID: " + str(p.key().id()) + "</li>\n")


usersPages = [('/createuser', CreateUser), ('/createuserwithparams', CreateUserWithParams), ('/listusers', ListUsers)]
