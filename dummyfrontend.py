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


# Not sure if this page is even necessary, this was more to practice how to use Jinja and javascript together
# Change it, add links, whatever.
# DO NOT DELETE IT! (or it's html page) It's a pretty good template
class UserWasCreated(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        createuser = '/createuser?phone=' + self.request.get("phone")

        template_values = {
            'createuser': createuser
        }

        template = JINJA_ENVIRONMENT.get_template('userwascreated.html')
        self.response.write(template.render(template_values))


# Copy-pasted from mpusersforms.py
class CreateUserForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        # No Jinja because this was directly copy-pasted
        self.response.write(
            """
              <div>It looks like you don't have an account with us yet!</div>
              <div>Fill in the form below to get started.</div>
              <br>

              <form method="get" action="/userwascreated">
                Enter phone number:<br>
                <div><input type="text" name="phone"></div>
                <div><input type="submit" value="Create Account"></div>
              </form>
            """)


# Copy-pasted from plansforms.py
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
        getPlansLink = '/plansbyuserid?userid=' + userid

        template_values = {
            'newPlanURL': newPlanLink,
            'getPlansURL': getPlansLink
        }

        template = JINJA_ENVIRONMENT.get_template('currentplans.html')
        self.response.write(template.render(template_values))


# Converts the string representation that the form input accepts into an actual datetime
def convertInputToDatetime(str):
    f = "%Y-%m-%dT%H:%M"
    return datetime.datetime.strptime(str, f)


# NOT DONE YET
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