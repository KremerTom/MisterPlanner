# The python for the page for the entirety of the dummy front end,

import os
import urllib
import webapp2
import jinja2
import json
import datetime
from google.appengine.api import users

import mpusers


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



# Redirect to the first page the user should see, depending on whether they have already
# created an account or not.
class FirstPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        googleid = users.get_current_user().user_id()

        userid = mpusers.userIdFromGoogleId(googleid)

        if userid is None:
            return self.redirect('/createuserform')
        else:
            path = '/currentplans?userid=' + userid
            return self.redirect(path)


# An in-between page that submits form data and parses the response json for the main front page.
class UserWasCreated(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        createuser = '/createuser?phone=' + self.request.get("phone")

        template_values = {
            'createuser': createuser
        }

        template = JINJA_ENVIRONMENT.get_template('userwascreated.html')
        self.response.write(template.render(template_values))


class CreateUserForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        template_values = {
            'redirectURL': '/userwascreated'
        }

        template = JINJA_ENVIRONMENT.get_template('createuserform.html')
        self.response.write(template.render(template_values))


class CreatePlanForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        template_values = {
            'redirectURL': '/planwascreated'
        }

        template = JINJA_ENVIRONMENT.get_template('createplanform.html')
        self.response.write(template.render(template_values))


# This is supposed to act as the front page, listing all of the plans for that user
class CurrentPlans(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'


        newPlanLink = '/createplanform'

        userid = self.request.get("userid")
        if userid is None or userid == "undefined":
            userid = mpusers.userIdFromGoogleId(users.get_current_user().user_id())
            # return self.redirect('/currentplans?userid=' + userid)

        # Weird bug where after creating account (including one that was a shadow account),
        # the userid is undefined. The next line of code is a TEMPORARY FIX.
        userid = mpusers.userIdFromGoogleId(users.get_current_user().user_id())
        getPlansLink = '/getplansandinvites?userid=' # + userid
        getPlanLink = '/getplanbyid?planid='
        respondToInviteLink = '/respondtoinvite?userid='
        respondToInviteLink2 = '&planid='
        respondToInviteLink3 = '&response='

        template_values = {
            'newPlanURL': newPlanLink,
            'getPlansURL': getPlansLink,
            'userId': userid,
            'getOnePlanURL': getPlanLink,
            'respondToInviteURL': respondToInviteLink,
            'respondToInviteURL2': respondToInviteLink2,
            'respondToInviteURL3': respondToInviteLink3
        }

        template = JINJA_ENVIRONMENT.get_template('currentplans.html')
        self.response.write(template.render(template_values))

        self.response.write("<a href=\"" + users.CreateLogoutURL("./googleuser") + "\">Logout</a>")


# Converts the string representation that the form input accepts into an actual datetime
def convertInputToDatetime(str):
    f = "%Y-%m-%dT%H:%M"
    return datetime.datetime.strptime(str, f)


# An "in between" page that calls the API to create the plan, then redirects to the front page
class PlanWasCreated(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        url = self.request.url
        index = url.index("?")
        path = url[index:]

        url = '/createplan' + path

        template_values = {
            'createPlanURL': url
        }

        template = JINJA_ENVIRONMENT.get_template('planwascreated.html')
        self.response.write(template.render(template_values))


pages = [('/currentplans', CurrentPlans), ('/createplanform', CreatePlanForm), ('/createuserform', CreateUserForm), ('/userwascreated', UserWasCreated),
         ('/firstpage', FirstPage), ('/planwascreated', PlanWasCreated)]