# The python for the page for the entirety of the dummy front end,
# EXCEPT for the two forms we had already made, however, I think they can be transferred here
# and re-written in jinja as well, if we're willing to be that consistent/care enough.
#

import os
import urllib
import webapp2
import jinja2
import json
import mpusersforms
import plansforms


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Not sure if this page is even necessary, this was more to practice how to use Jinja and javascript together
# Change it, add links, whatever.
# DO NOT DELETE IT! (or it's html page) It's a pretty good template
class UserWasCreated(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        url = '/createuser?phone=' + self.request.get("phone")

        template_values = {
            'url': url
        }

        template = JINJA_ENVIRONMENT.get_template('userwascreated.html')
        self.response.write(template.render(template_values))




# Make this standard? i.e. whatever the html is called.pages
pages = [('/userwascreated', UserWasCreated)] + mpusersforms.usersForms + plansforms.plansForms