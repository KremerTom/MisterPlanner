from google.appengine.ext import db
from google.appengine.api import users


import mpusers
import invites
import datetime
import webapp2
import json


class Plan(db.Model):
    planId = db.StringProperty()
    authorId = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    pointOfNoReturn = db.DateTimeProperty(required=True)
    eventDate = db.DateTimeProperty(required=True)
    status = db.BooleanProperty(required=False)



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
        return temp_plan
    else:
        print newTitle + " already exists"
        return None



# Converts the string representation that the form input accepts into an actual datetime
def convertInputToDatetime(str):
    f = "%Y-%m-%dT%H:%M"
    return datetime.datetime.strptime(str, f)


# Handles the submitted form data for creating a new plan.
class CreatePlan(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        title = self.request.get("title")

        # This won't work when we change our front-end, since it modifies the way that the html form submits dates/times
        eventDate = convertInputToDatetime(self.request.get("eventtime"))
        pointOfNoReturn = convertInputToDatetime(self.request.get("responsetime"))

        userKey = mpusers.userIdFromGoogleId(users.get_current_user().user_id())

        # try to create the plan
        plan = createPlan(userKey, title, pointOfNoReturn, eventDate)
        if plan is not None:
            self.response.write(json.dumps(convertPlanToDictionary(plan)))
            OGuserid = mpusers.userIdFromGoogleId(users.get_current_user().user_id())
            invites.createInvite(OGuserid, plan.planId)
            invitedNums = self.request.get("invites").split()
            for num in invitedNums:
                userid = mpusers.getUserIdByNumber(num)
                if userid is None:
                    userid = mpusers.createShadowUser(num).userId
                invites.createInvite(userid, plan.planId)
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
    dict['Final Verdict'] = plan.status

    return dict



class ConfirmPlan(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        userId = mpusers.userIdFromGoogleId(users.get_current_user().user_id())
        planId = self.request.get("planid")
        q = Plan.all()
        q.filter("planId =", planId)
        plan = q.get()

        if plan.authorId != userId:
            self.response.write("You are not the host of this event.")
            return

        toProceed = self.request.get("verdict")
        proceed = (toProceed == 'True' or toProceed == 'true')

        plan.status = proceed

        plan.put()

        self.response.write(json.dumps(convertPlanToDictionary(plan)))



# Respond with JSON object of all the plans that a specific user is invited to
# Automatically includes plans that that user had created
class ListAllPlans(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        userId = self.request.get("userid")
        q = invites.Invite.all()
        q.filter("userId =", userId)

        temp = []

        for p in q.run():
            qq = Plan.all()
            qq.filter("planId =", p.planId)
            temp.append(convertPlanToDictionary(qq.get()))

        plans = {"plans":temp}
        self.response.write(json.dumps(plans))


# get one specific plan, by planID
# The JSON response also includes every invitation under the key "responses"
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
            dict = {"plan": convertPlanToDictionary(plan)}
            dict["responses"] = invites.listInvites(planid)
            self.response.write(json.dumps(dict))

plansAPI = [('/listplans', ListAllPlans), ('/createplan', CreatePlan), ('/getplanbyid', GetPlanByID), ('/confirmplan', ConfirmPlan)]
