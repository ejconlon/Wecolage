from common import *

import cgi, sessions, formatting

from paste_model import Paste

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Home(sessions.PersistentRequestHandler):  
	def get(self):
		self.init_session()
		if self.do_redirect(): return
		
		user = self.get_key('user')
		pastes_query = Paste.gql("WHERE owner=:owner ORDER BY date_created DESC",
									owner=user)
		pastes = pastes_query.fetch(10)
		
		self.template_values.update({
			'explain': True,
			'formats': formatting.formats_ordered,
			'pastes': pastes
		})
		path = get_template_path('index.html')
		self.response.out.write(template.render(path, self.template_values, debug=True))
		
class About(sessions.PersistentRequestHandler):  
	def get(self):
		self.init_session()
		if self.do_redirect(): return
		path = get_template_path('about.html')
		self.response.out.write(template.render(path, self.template_values, debug=True))

class FourOhFour(sessions.PersistentRequestHandler):  
	def get(self):
		self.init_session()
		if self.do_redirect(): return
		self.error(404)
		path = get_template_path('404.html')
		self.response.out.write(template.render(path, self.template_values, debug=True))
		
class Login(webapp.RequestHandler):  
	def get(self):
		self.redirect(users.create_login_url(self.request.uri))
		return
		
class Logout(webapp.RequestHandler):  
	def get(self):
		self.redirect(users.create_logout_url(self.request.uri))
		return