from google.appengine.ext import db

import datetime
import webapp2


class User(db.Model):
    email = db.StringProperty(required=True)

class Plan(db.Model):
    authorId = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    pointOfNoReturn = db.DateTimeProperty(required=True)
    eventDate = db.DateTimeProperty(required=True)

class UsersToPlans(db.Model):
    userId = db.StringProperty(required=True)
    planId = db.StringProperty(required=True)
    attending = db.BooleanProperty(required=False)

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


def createPlan(newAuthorId, newTitle, newPointOfNoReturn, newEventDate):
    plan = Plan(authorId = newAuthorId, title = newTitle, pointOfNoReturn = newPointOfNoReturn, eventDate = newEventDate)
    q = Plan.all()
    q.filter("title =", newTitle)
    q.filter("eventDate =", newEventDate)
    q.filter("authorId =", newAuthorId)

    if q.get() is None:
        plan.put()
        print "successfully wrote " + newTitle
        return True
    else:
        print newTitle + " already exists"
        return False

# create a new plan according to URL parameters
class CreatePlan(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="post" action="/planformhandler">
                <div>Your Email Address: <input type="text" name="email"></div>
                <div>Name of Event: <input type="text" name="title"></div>
                <div>When is your event? <input type="datetime-local" name="eventtime">
                    </div>
                <div>By when do you need your responses? <input type="datetime-local" name="responsetime">
                    </div>
                <div><input type="submit" value="Create Plan"></div>
              </form>""")


# Handles the submitted form data for creating a new plan.
class PlanFormHandler(webapp2.RequestHandler):
    def post(self):
        emailAddress=self.request.get("email")
        title = self.request.get("title")
        eventDate = convertInputToDatetime(self.request.get("eventtime"))
        pointOfNoReturn = convertInputToDatetime(self.request.get("responsetime"))

        # Check if the entered email is actually a member
        q = User.all()
        q.filter("email = ", emailAddress)
        p = q.get()
        if p is None:
            self.response.write("<div>That's not a valid email</div>")
            return

        # CHANGED TO AUTHOR'S EMAIL
        # Use that email's key
        userKey = str(p.key())

        # try to create the plan
        if createPlan(emailAddress, title, pointOfNoReturn, eventDate):
            self.response.write("success")
        else:
            self.response.write(title + " already exists")

# Converts the string representation that the form input accepts into an actual datetime
def convertInputToDatetime(str):
    f = "%Y-%m-%dT%H:%M"
    return datetime.datetime.strptime(str, f)

class ListPlans(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/html; charset=utf-8'


        f = "%m/%d/%Y %H:%M"

        #write all plans in system
        q = Plan.all()
        for p in q.run():
            self.response.write("<li>Email: " + p.authorId + "<br>Event Title: " + p.title + "<br>Event Start Time: " + p.eventDate.strftime(f) + "<br>Event Response Deadline: " + p.pointOfNoReturn.strftime(f) + "</li>\n")


# doesn't do jack shit right now
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.headers['EasterEgg'] = 'HOLLYWOOOOOOOOOOD'
        # Tom: Not 'RickyTickyTavvy'?

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createuser', CreateUser),
    ('/createuserwithparams', CreateUserWithParams),
    ('/listusers', ListUsers),
    ('/createplan', CreatePlan),
    ('/planformhandler', PlanFormHandler),
    ('/listplans', ListPlans)
], debug=True)
