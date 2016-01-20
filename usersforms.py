import users
import webapp2

class CreateUserWithParams(webapp2.RequestHandler):
    def post(self):
        phone=self.request.get("phone")
        self.response.out.write('<li>' + phone + '</li>')

        if users.createUser(phone):
            self.response.write("success")
        else:
            self.response.write("user already exists")

# create a new user with phone set to "phone" URL param
class CreateUserForm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        self.response.write(
            """<form method="post" action="/createuserwithparams">
                Enter phone number:<br>
                <div><input type="text" name="phone"></div>
                <div><input type="submit" value="Create Account"></div>
              </form>""")


usersForms = [('/createuserwithparams', CreateUserWithParams), ('/createuserform', CreateUserForm)]
