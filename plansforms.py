import webapp2

class CreatePlanForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="get" action="/createplan">
                <div>Name of Event: <input type="text" name="title"></div>
                <div>When is your event? <input type="datetime-local" name="eventtime">
                    </div>
                <div>By when do you need your responses? <input type="datetime-local" name="responsetime">
                    </div>
                <div>List the phone numbers of whomever you're inviting (space separated): <input type = "text" name = "invites"></div>
                <div><input type="submit" value="Create Plan"></div>
              </form>""")


plansForms = [('/createplanform', CreatePlanForm)]