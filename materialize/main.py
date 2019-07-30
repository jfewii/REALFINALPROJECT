import webapp2
import jinja2
import os
import time
from model import UserDataStore
from google.appengine.ext import ndb
from model import MessageDataStore

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        home_template = the_jinja_env.get_template('/homepage.html')
        self.response.write(home_template.render())

class LoginPage(webapp2.RequestHandler):
    def get(self):
        login_template = the_jinja_env.get_template('/login.html')
        error = self.request.get('error')
        new_dic = {
            'errormessage': error
        }
        self.response.write(login_template.render(new_dic))

    def post(self):
        username_query = UserDataStore.query()
        users = username_query.fetch()
        print(users)
        for x in users:
            if x.psw == self.request.get('psw') and x.username == self.request.get('uname'):
                self.redirect('/profile')
                return
        self.redirect('/login?error=not-found')
        return

class SignUpPage(webapp2.RequestHandler):
    def get(self):
        signup_template = the_jinja_env.get_template('/signup.html')
        self.response.write(signup_template.render())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('psw')
        passwordRepeat = self.request.get('psw-repeat')

        userlogin = UserDataStore(username=username, psw=password)
        userlogin.put()
        self.redirect('/login')

class ProfilePage(webapp2.RequestHandler):
        def get(self):
            profile_template = the_jinja_env.get_template('/profile.html')
            self.response.write(profile_template.render())

class FriendsPage(webapp2.RequestHandler):
    def get(self):
        friends_template = the_jinja_env.get_template('/friends.html')
        self.response.write(friends_template.render())

    def post(self):
        friends_template = the_jinja_env.get_template('/friends.html')
        status = self.request.get("CurrentStatus")
        timeStamp = self.request.get("StatusTime")

        messagestore = MessageDataStore(CurrentStatus=status)
        messagestore.put()
        time.sleep(0.1)

        status_query = MessageDataStore.query().order(-MessageDataStore.StatusTime)
        messagecollection = status_query.fetch()

        the_variable_dict = {
        'statuses': messagecollection,
        }
        self.response.write(friends_template.render(the_variable_dict))

class MessagesPage(webapp2.RequestHandler):
    def get(self):
        messages_template = the_jinja_env.get_template('/messages.html')
        self.response.write(messages_template.render())

class AboutPage(webapp2.RequestHandler):
    def get(self):
        about_template = the_jinja_env.get_template('/aboutus.html')
        self.response.write(about_template.render())

class SuggestionsPage(webapp2.RequestHandler):
    def get(self):
        suggestion_template = the_jinja_env.get_template('/suggestions.html')
        self.response.write(suggestion_template.render())



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/signup', SignUpPage),
    ('/profile', ProfilePage),
    ('/friends', FriendsPage),
    ('/messages', MessagesPage),
    ('/aboutus', AboutPage),
    ('/suggestions', SuggestionsPage),
], debug=True)
