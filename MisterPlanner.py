from google.appengine.ext import db

import datetime
import webapp2
import plans
import users

# doesn't do jack shit right now
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.headers['EasterEgg'] = 'HOLLYWOOOOOOOOOOD'
        # Tom: Not 'RickyTickyTavvy'?

mainPages = [('/', MainPage)]
allPages = mainPages + users.usersPages + plans.plansPages

app = webapp2.WSGIApplication(allPages, debug=True)
