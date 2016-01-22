from google.appengine.ext import db

import webapp2


class User(db.Model):
    userId = db.StringProperty()
    phoneNumber = db.PhoneNumberProperty(required=True)

def createUser(phone):
    user = User(phoneNumber = phone)
    q = User.all()
    q.filter("phoneNumber =", phone)

    if q.get() is None:
        user_key = user.put()

        temp_user = db.get(user_key)
        temp_user.userId = str(user_key.id())
        temp_user.put()

        print "successfully wrote " + temp_user.phoneNumber
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

        # write all users in system
        q = User.all()
        for p in q.run():
            self.response.write("<li>Phone: " + p.phoneNumber + ", ID: " + str(p.key().id()) + "</li>\n")

# get one specific user, by ID
class GetUserByID(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        userid = self.request.get("userid")

        # write only one specific user
        q = User.all()
        q.filter("userId =", userid)
        user = q.get()

        if user is None:
            self.response.write(userid + " doesn't exist")
        else:
            self.response.write(user.phoneNumber)


usersAPI = [('/createuser', CreateUser), ('/listusers', ListUsers), ('/getuserbyid', GetUserByID)]
