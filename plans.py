from google.appengine.ext import db

import users
import datetime
import webapp2
import json


class Plan(db.Model):
    planId = db.StringProperty()
    authorId = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    pointOfNoReturn = db.DateTimeProperty(required=True)
    eventDate = db.DateTimeProperty(required=True)

class UsersToPlans(db.Model):
    userId = db.StringProperty(required=True)
    planId = db.StringProperty(required=True)
    attending = db.BooleanProperty(required=False)

def createPlan(newAuthorId, newTitle, newPointOfNoReturn, newEventDate):

    # if newPointOfNoReturn > newEventDate:
    #     print "You can't have the response time after the event start time"
    #     return
    #
    # if newEventDate < datetime.datetime.now() or newPointOfNoReturn < datetime.datetime.now():
    #     print "You can't use dates or times from the past!"
    #     return

    plan = Plan(authorId = newAuthorId, title = newTitle, pointOfNoReturn = newPointOfNoReturn, eventDate = newEventDate)
    q = Plan.all()
    q.filter("title =", newTitle)
    q.filter("eventDate =", newEventDate)
    q.filter("authorId =", newAuthorId)

    if q.get() is None:
        plan_key = plan.put()

        temp_plan = db.get(plan_key)
        temp_plan.planId = str(plan_key.id())
        temp_plan.put()

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
    def get(self):
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

def convertPlanToDictionary(plan):
    f = "%m/%d/%Y %H:%M"

    dict = {}
    dict['Plan ID'] = str(plan.planId)
    dict['Host ID'] = str(plan.authorId)
    dict['Title'] = plan.title
    dict['Respond By'] = plan.pointOfNoReturn.strftime(f)
    dict['Event Date'] = plan.eventDate.strftime(f)

    return dict

# print a list of all the plans in the database
class ListAllPlans(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        #write all plans in system
        q = Plan.all()

        temp = []

        for p in q.run():
            temp.append(convertPlanToDictionary(p))

        plans = {"plans":temp}
        self.response.write(json.dumps(plans))

# get one specific plan, by planID
class GetPlanByID(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        planid = self.request.get("planid")

        q = Plan.all()
        q.filter("planId =", planid)
        plan = q.get()

        if plan is None:
            self.response.write(planid + " doesn't exist")
        else:
            self.response.write(json.dumps(convertPlanToDictionary(plan)))

plansAPI = [('/listplans', ListAllPlans), ('/createplan', CreatePlan), ('/getplanbyid', GetPlanByID)]
