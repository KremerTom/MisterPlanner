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

# Tom: question: Is this only to relate plans with their creators? or is this
# with anyone involved? Like, should their be a third boolean property 
# called Attending(True/False, but not required)?
class UsersToPlans(db.Model):
    userId = db.StringProperty(required=True)
    planId = db.StringProperty(required=True)

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

# create a new user with email set to "email" URL param
class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        
        if createUser(self.request.get("email")):
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
            self.response.write("<li>Email: " + p.email + ", ID: " + str(p.key().id()) + "</li>\n")


def createPlan(newAuthorId, newTitle, newPointOfNoReturn, newEventDate):
    plan = Plan(authorId = newAuthorId, title = newTitle, pointOfNoReturn = newPointOfNoReturn, eventDate = newEventDate)
    q = Plan.all()
    q.filter("title =", newTitle)
    q.filter("eventDate =", newEventDate)

    # Tom: This doesn't actually identify if the plan already exists.
    # If two groups are trying to organize going to the same showtime...
    # But that's not urgent

    # Tom: I would add
    q.filter("authorId =", newAuthorId)
    
    if q.get() is None:
        plan.put()
        print "successfully wrote " + newTitle
        return True
    else:
        print eventTitle + " already exists"
        return False

# create a new plan according to URL parameters
class CreatePlan(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        # retrieve URL parameter values
        emailAddress = self.request.get("email")
        title = self.request.get("title")
        eventDate = datetime.datetime.now()
        pointOfNoReturn = datetime.datetime.now()
        
        # get a string representation of the key for the user creating this plan
        q = User.all()
        q.filter("email = ", emailAddress)
        p = q.get()
        userKey = str(p.key())
        
        # try to create the plan
        if createPlan(userKey, title, pointOfNoReturn, eventDate):
            self.response.write("success")
        else:
            self.response.write("plan already exists")




# doesn't do jack shit right now
class MainPage(webapp2.RequestHandler):
    def get(self):        
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.headers['EasterEgg'] = 'HOLLYWOOOOOOOOOOD'
        # Tom: Not 'RickyTickyTavvy'?

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createuser', CreateUser),
    ('/listusers', ListUsers),
    ('/createplan', CreatePlan),
], debug=True)
