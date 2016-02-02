import webapp2


# create a new user with phone set to "phone" URL param
class CreateUserForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="get" action="/createuser">
                Enter phone number:<br>
                <div><input type="text" name="phone"></div>
                <div><input type="submit" value="Create Account"></div>
              </form>""")


usersForms = [('/createuserform', CreateUserForm)]
