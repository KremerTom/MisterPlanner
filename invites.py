from google.appengine.ext import db
from google.appengine.api import users

import mpusers
import plans
import datetime
import webapp2
import json



class Invite(db.Model):
    userId = db.StringProperty(required=True)
    planId = db.StringProperty(required=True)
    response = db.BooleanProperty(required=False)
    responseTime = db.DateTimeProperty(required=False)

def createInvite(newUserId, newPlanId):
    invite = Invite(userId = newUserId, planId = newPlanId)

    q = Invite.all()
    q.filter("userId =", newUserId)
    q.filter("planId =", newPlanId)

    if q.get() is None:
        invite.put()
        return invite
    else:
        print("That invite already exists")
        return None


class CreateInvite(webapp2.RequestHandler):
    def get(self):
        userId = self.request.get("userid")
        planId = self.request.get("planid")

        invite = createInvite(userId, planId)
        if invite is not None:
            self.response.write(json.dumps(convertInviteToDictionary(invite)))
        else:
            self.response.write("That invite already exists")


def respondToInvite(userId, planId, response):
    now = datetime.datetime.now()

    qq = plans.Plan.all()
    qq.filter("planId =", planId)
    thisPlan = qq.get()
    if thisPlan is not None and thisPlan.pointOfNoReturn < now:
        print("It's too late to respond to that event.")
        return None

    q = Invite.all()
    q.filter("userId =", userId)
    q.filter("planId =", planId)
    thisInvite = q.get()

    if thisInvite is None:
        return None
    else:
        thisInvite.response = response
        thisInvite.responseTime = datetime.datetime.now()
        thisInvite.put()
        return thisInvite


class RespondToInvite(webapp2.RequestHandler):
    def get(self):
        userId = self.request.get("userid")
        planId = self.request.get("planid")
        response = self.request.get("response").lower() == 'yes'

        updatedInvite = respondToInvite(userId, planId, response)
        if updatedInvite:
            self.response.write(json.dumps(convertInviteToDictionary(updatedInvite)))
        else:
            self.response.write("That invite does not exist")


def listInvites(planid):
    temp = []

    q = Invite.all()
    q.filter("planId =", planid)

    for i in q.run():
        temp.append(convertInviteToDictionary(i))

    if len(temp) == 0:
        self.response.write("That event has no invites or does not exist!")
        return

    return temp


class ListInvites(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        planid = self.request.get("planid")

        dict = {"responses": listInvites(planid)}

        self.response.write(json.dumps(dict))

# TODO:
# Add some comments :)

def getInvite(planid, userid):
    q = Invite.all()
    q.filter("planId =", planid)
    q.filter("userId =", userid)

    temp = q.get()
    if temp:
        dict = convertInviteToDictionary(temp)
        return dict
    else:
        self.response.write("That invite does not exist!")
        return None


# Like PlansByUserID (in plans.py), but also returns user specific invitation information for each plan.
# This is useful for having the information about both the plan and the invited user's status at the same time.
class GetPlansAndInvites(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        userid = self.request.get("userid")
        if userid is None:
            userid = mpusers.userIdFromGoogleId(users.get_current_user().user_id())


        plandicts = plans.plansByUserId(userid)
        print plandicts
        # planid = self.request.get("planid")

        for plan in plandicts:
            thisInvite = getInvite(plan['PlanID'], userid)
            print thisInvite
            plan['Response'] = thisInvite['Response']
            plan['InvitedID'] = thisInvite['UserID']

        dict = {"plans": plandicts}

        self.response.write(json.dumps(dict))



def convertInviteToDictionary(invite):
    f = "%m/%d/%Y %H:%M"

    dict = {}
    dict['UserID'] = invite.userId
    dict['PlanID'] = invite.planId
    dict['Response'] = invite.response
    dict['ResponseTime'] = invite.responseTime
    if invite.responseTime is not None:
        dict['ResponseTime'] = invite.responseTime.strftime(f)

    return dict



invitesAPI = [('/createinvite', CreateInvite), ('/respondtoinvite', RespondToInvite), ('/listinvites', ListInvites), ('/getplansandinvites', GetPlansAndInvites)]
