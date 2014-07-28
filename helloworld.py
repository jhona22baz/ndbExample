import cgi
import urllib

import webapp2

from google.appengine.ext import ndb

class Address(ndb.Model):
  type = ndb.StringProperty() # E.g., 'home', 'work'
  street = ndb.StringProperty()
  city = ndb.StringProperty()

class Contact(ndb.Model): #M
  """Models an individual Guestbook entry with content, date and something."""
  content = ndb.StringProperty()
  addresses = ndb.StructuredProperty(Address, repeated=True)
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)



class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')    
    guestbook_name = self.request.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    contacts = Contact.query_book(ancestor_key).fetch(20) 

    for contact in contacts:
      self.response.out.write('Book_name %s, </br>'%guestbook_name)
      self.response.out.write('content -> %s,</br>' % cgi.escape(contact.content))#m
      self.response.out.write(' Address-> %s,</br> '  % contact.addresses)#m
      self.response.out.write(' date %s </br></br>' % contact.date)#m

      

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div>comentarios -> <textarea name="content" rows="3" cols="60"></textarea></div>
            <div>something -><textarea name="something" rows="2" cols="20"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>

          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                    cgi.escape(guestbook_name)))

class SubmitForm(webapp2.RequestHandler):
  def post(self):
    # We set the parent key on each 'Contact' to ensure each guestbook's #M
    # contacts are in the same entity group.
    guestbook_name = self.request.get('guestbook_name') #m
    contact = Contact(parent=ndb.Key("Book", guestbook_name or "*notitle*"), #m M
                        content = self.request.get('content'),                        
                        addresses=[Address(type='Home', street = 'Garza Sada',city='Monterrey'),
                               Address(type='work',street='Cozumel',city='Guadalupe')])
    contact.put()#m
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', SubmitForm)
])