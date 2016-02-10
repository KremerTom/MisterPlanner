from google.appengine.ext import db
from google.appengine.api import users

import webapp2
import json


class User(db.Model):
    userId = db.StringProperty()
    phoneNumber = db.PhoneNumberProperty(required=True)
    googleId = db.StringProperty()


# CREATE USER NOW AUTOMATICALLY ADDS A GOOGLE ID
# there's both a function and an API endpoint to get a misterplanner user ID from the google user ID
# every front-end call to an API that shows user specific data must include the user's ID, and the user's
# ID can now easily be retrieved from the Google ID of the logged in user.
#
# Create user still requires a phone number.


# TODO:
# Write API for converting a shadow account into a real account

def createUser(phone):
    user = User(phoneNumber = phone)

    q = User.all()
    # q.filter("phoneNumber =", phone)
    googleId = users.get_current_user().user_id()
    q.filter("googleId =", googleId)

    if q.get() is None:
        user_key = user.put()

        temp_user = db.get(user_key)
        temp_user.userId = str(user_key.id())

        # add current Google ID as the "googleId"
        temp_user.googleId = googleId

        temp_user.put()

        print "successfully wrote " + temp_user.phoneNumber
        return temp_user
    else:
        print phone + " already exists"
        return None


# The only difference between this and createUser is the lack of googleId
def createShadowUser(phone):
    user = User(phoneNumber = phone)

    q = User.all()
    q.filter("phoneNumber =", phone)

    if q.get() is None:
        user_key = user.put()

        temp_user = db.get(user_key)
        temp_user.userId = str(user_key.id())

        temp_user.put()

        print "successfully wrote " + temp_user.phoneNumber
        return temp_user
    else:
        print phone + " already exists"
        return None


# create a new user with phone set to "phone" URL param
class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        user = createUser(self.request.get("phone"))
        if user is not None:
            self.response.write(json.dumps(convertUserToDictionary(user)))
        else:
            self.response.write("user already exists")



# helper function to return a user's ID based on the Google ID
def userIdFromGoogleId(googleId):
    # get only one specific user
    q = User.all()
    q.filter("googleId =", googleId)
    temp_user = q.get()

    if temp_user is not None:
        return temp_user.userId
    else:
        return None


class UserIdFromGoogleId(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        userId = userIdFromGoogleId(self.request.get("googleid"))

        if userId is not None:
            self.response.write(userId)
        else:
            self.response.write("user doesn't exist")


# list all users
class ListUsers(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        # write all users in system
        q = User.all()

        temp = []
        for p in q.run():
            temp.append(convertUserToDictionary(p))
            # self.response.write("<li>Phone: " + p.phoneNumber + ", ID: " + str(p.key().id()) + "</li>\n")
        users = {"users": temp}
        self.response.write(json.dumps(users))


# get one specific user, by ID
class GetUserByID(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        userid = self.request.get("userid")

        # get only one specific user
        q = User.all()
        q.filter("userId =", userid)
        user = q.get()

        if user is None:
            self.response.write(userid + " doesn't exist")
        else:
            self.response.write(json.dumps(convertUserToDictionary(user)))


# Looks up a user account by phone number, and returns the userID of the user if it exists.
class DoesAccountExist(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        phone = self.request.get("phone")

        # write only one specific user
        q = User.all()
        q.filter("phoneNumber =", phone)
        user = q.get()

        if user is None:
            # Could returning the JSON version of NULL
            self.response.write(json.dumps(user))
            return None
        else:
            # Return JSON string
            self.response.write(json.dumps(convertUserToDictionary(user)))


def getUserIdByNumber(phone):
    q = User.all()
    q.filter("phoneNumber =", phone)
    user = q.get()

    if user is None:
        return None
    else:
        return user.userId


def convertUserToDictionary(user):
    conversion = {'User Id': str(user.userId), 'Phone Number': str(user.phoneNumber), 'Google Id': str(user.googleId)}
    return conversion


# debug API endpoint to help with Google auth
class GoogleUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        user = users.get_current_user()
        if not user:
            self.response.write("you're not signed in")
        else:
            self.response.write("<p>hello, %s!" % user.nickname() + "</p>")
            self.response.write("<p>email is %s!" % user.email() + "</p>")
            self.response.write("<p>google user id is %s!" % user.user_id() + "</p>")
            self.response.write("<p>misterplanner user id is %s!" % userIdFromGoogleId(user.user_id()) + "</p>")

            self.response.write("<a href=\"" + users.CreateLogoutURL("./googleuser") + "\">Logout</a>")



usersAPI = [('/createuser', CreateUser), ('/listusers', ListUsers), ('/getuserbyid', GetUserByID), ('/doesaccountexist', DoesAccountExist), ('/useridfromgoogleid', UserIdFromGoogleId), ('/googleuser', GoogleUser)]
