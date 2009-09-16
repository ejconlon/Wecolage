from common import *

import cgi, sessions, formatting

from paste_model import Paste

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Home(webapp.RequestHandler):  
	def get(self):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
		
		user = sessions.get_user(session)
		
		pastes_query = Paste.gql("WHERE owner=:owner ORDER BY date_created DESC",
									owner=user)
		pastes = pastes_query.fetch(10)
		
		template_values = {
			'session': session,
			'flash': flash,
			'explain': True,
			'formats': formatting.formats_ordered,
			'pastes': pastes
		}
		
		path = get_template_path('index.html')
		self.response.out.write(template.render(path, template_values, debug=True))