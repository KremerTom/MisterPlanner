from google.appengine.ext import db

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

# create a new user with phone set to "phone" URL param
class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        if createUser(self.request.get("phone")):
            self.response.write("success")
        else:
            self.response.write("user already exists")

# list all users
class ListUsers(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        #write all users in system
        q = User.all()
        for p in q.run():
            self.response.write("<li>Phone: " + p.phoneNumber + ", ID: " + str(p.key().id()) + "</li>\n")


usersAPI = [('/createuser', CreateUser), ('/listusers', ListUsers)]
