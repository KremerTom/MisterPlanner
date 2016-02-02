from google.appengine.ext import db

import users
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

    qq = Plan.all()
    qq.filter("planId =", planId)
    thisPlan = qq.get()
    if thisPlan is not None and thisPlan.pointOfNoReturn < now:
        print("It's too late to respond to that event.")
        return None

    q = Invite.all()
    q.filter("userId =", userId)
    q.filter("planId =", planId)

    if q.get() is None:
        return None
    else:
        invite = q.get()
        invite.response = response
        invite.responseTime = datetime.datetime.now()
        invite.put()
        return invite


class RespondToInvite(webapp2.RequestHandler):
    def get(self):
        userId = self.request.get("userid")
        planId = self.request.get("planid")
        response = (self.request.get("response") == 'True' or self.request.get("response") == 'true')

        updatedInvite = respondToInvite(userId, planId, response)
        if updatedInvite:
            self.response.write(json.dumps(convertInviteToDictionary(updatedInvite)))
        else:
            self.response.write("That invite does not exist")



# TODO:
# List all invitations to a certain event
# Modify createinvite to discriminate between phone numbers that already have accounts and those who don't



def convertInviteToDictionary(invite):
    f = "%m/%d/%Y %H:%M"

    dict = {}
    dict['User ID'] = invite.userId
    dict['Plan ID'] = invite.planId
    dict['Response'] = invite.response
    dict['Response Time'] = invite.responseTime
    if invite.responseTime is not None:
        dict['Response Time'] = invite.responseTime.strftime(f)

    return dict



invitesAPI = [('/createinvite', CreateInvite), ('/respondtoinvite', RespondToInvite)]