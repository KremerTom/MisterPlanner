from google.appengine.ext import db

import users
import datetime
import webapp2


class Plan(db.Model):
    authorId = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    pointOfNoReturn = db.DateTimeProperty(required=True)
    eventDate = db.DateTimeProperty(required=True)

class UsersToPlans(db.Model):
    userId = db.StringProperty(required=True)
    planId = db.StringProperty(required=True)
    attending = db.BooleanProperty(required=False)

def createPlan(newAuthorId, newTitle, newPointOfNoReturn, newEventDate):

    if newPointOfNoReturn > newEventDate:
        print "You can't have the response time after the event start time"
        return

    if newEventDate < datetime.datetime.now() or newPointOfNoReturn < datetime.datetime.now():
        print "You can't use dates or times from the past!"
        return

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



# Converts the string representation that the form input accepts into an actual datetime
def convertInputToDatetime(str):
    f = "%Y-%m-%dT%H:%M"
    return datetime.datetime.strptime(str, f)


# Handles the submitted form data for creating a new plan.
class CreatePlan(webapp2.RequestHandler):
    def post(self):
        phone=self.request.get("phone")
        title = self.request.get("title")
        eventDate = convertInputToDatetime(self.request.get("eventtime"))
        pointOfNoReturn = convertInputToDatetime(self.request.get("responsetime"))

        # Check if the entered phone number is actually a member
        # Necessary here to create the new plan with the owner's user key
        q = users.User.all()
        q.filter("phoneNumber = ", phone)
        p = q.get()
        if p is None:
            self.response.write("<div>We don't have any user with that phone number</div>")
            return

        # CHANGED TO AUTHOR'S PHONE
        # Use that phone's key
        userKey = str(p.key().id())

        # try to create the plan
        if createPlan(userKey, title, pointOfNoReturn, eventDate):
            self.response.write("success")
        else:
            self.response.write(title + " already exists")

class ListPlans(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/html; charset=utf-8'


        f = "%m/%d/%Y %H:%M"

        #write all plans in system
        q = Plan.all()
        for p in q.run():
            self.response.write("<li>Phone number: " + p.authorId + "<br>Event Title: " + p.title + "<br>Event Start Time: " + p.eventDate.strftime(f) + "<br>Event Response Deadline: " + p.pointOfNoReturn.strftime(f) + "</li>\n")


plansAPI = [('/listplans', ListPlans), ('/createplan', CreatePlan)]
