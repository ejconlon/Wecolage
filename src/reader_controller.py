from common import *

import cgi, sessions

from paste_model import Paste

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Reader(webapp.RequestHandler):
	def get(self, code):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
		
		paste = Paste.get_by_code(cgi.escape(code))
		if paste is None:
			logger.error("PASTE "+code+" NOT FOUND")
			self.redirect('/404')
			return
			
		template_values = {
			'session': session,
			'flash': flash,
			'paste': paste,
			'paste_url': paste.get_url()
		}
		
		path = get_template_path('view_paste.html')
		self.response.out.write(template.render(path, template_values, debug=True))