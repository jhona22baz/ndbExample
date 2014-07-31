# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Contacts' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Address(ndb.Model):
  label = ndb.StringProperty() # E.g., 'home', 'work'
  street = ndb.StringProperty()
  city = ndb.StringProperty()

class Contact(ndb.Model): #M
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        contacts_query = Contact.query(ancestor=guestbook_key(guestbook_name)).order(-Contact.date) #m M M
        contacts = contacts_query.fetch(10)#m m 

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'contacts': contacts,#m m
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Contact' to ensure each Contact
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        contact = Contact(parent=guestbook_key(guestbook_name))#m M

        if users.get_current_user():
            contact.author = users.get_current_user() #m

        contact.content = self.request.get('content')#m                
        label_ = self.request.get('label')
        street_ = self.request.get('street')
        city_ = self.request.get('city')
        contact.addresses= [Address(label=label_,street=street_,city=city_),]
        contact.put()#m

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)
