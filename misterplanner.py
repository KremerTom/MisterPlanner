import webapp2
import plans
import mpusers
import invites
import dummyfrontend


# doesn't do jack shit right now
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.headers['EasterEgg'] = 'HOLLYWOOOOOOOOOOD'
        # Tom: Not 'RickyTickyTavvy'?
        # THANKS PENCILVESTER!

        return self.redirect('/firstpage')

mainPages = [('/', MainPage)]
allPages = mainPages + mpusers.usersAPI + plans.plansAPI + invites.invitesAPI + dummyfrontend.pages

app = webapp2.WSGIApplication(allPages, debug=True)
