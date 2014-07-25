import cgi
import urllib

import webapp2

from google.appengine.ext import ndb


class Greeting(ndb.Model):
  """Models an individual Guestbook entry with content, date and something."""
  something = ndb.StringProperty()
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')    
    guestbook_name = self.request.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(20)

    for greeting in greetings:
      self.response.out.write('content -> %s,' % cgi.escape(greeting.content))
      self.response.out.write(' something -> %s </br>'  % greeting.something)
      

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div>content -> <textarea name="content" rows="3" cols="60"></textarea></div>
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
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        content = self.request.get('content'),something = self.request.get('something'))
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', SubmitForm)
])