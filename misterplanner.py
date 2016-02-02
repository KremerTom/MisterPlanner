import webapp2
import plans
import mpusers
import invites
import mpusersforms
import plansforms


# doesn't do jack shit right now
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.headers['EasterEgg'] = 'HOLLYWOOOOOOOOOOD'
        # Tom: Not 'RickyTickyTavvy'?
        # THANKS PENCILVESTER!

mainPages = [('/', MainPage)]
allPages = mainPages + mpusers.usersAPI + mpusersforms.usersForms + plans.plansAPI + plansforms.plansForms + invites.invitesAPI

app = webapp2.WSGIApplication(allPages, debug=True)
