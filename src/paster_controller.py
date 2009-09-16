from common import *

import cgi, sessions

from paste_model import Paste

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Paster(webapp.RequestHandler):
	def post(self):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
		
		paste = Paste()
		paste.owner = sessions.get_user(session)
		paste.name = cgi.escape(self.request.get('name'))
		paste.content = cgi.escape(self.request.get('content'))
		paste.format = cgi.escape(self.request.get('format'))
		paste.hidden = (self.request.get('hidden')=="on")
		paste.parsed_content = formatting.highlight_with_longname(
								self.request.get('content'), paste.format)
		
		paste.save_new(cgi.escape(self.request.get('password')))
		self.redirect('/read/'+paste.code)

	def get(self):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
			
		template_values = {
			'session': session,
			'flash': flash
		}
		
		path = get_template_path('new_paste.html')
		self.response.out.write(template.render(path, template_values, debug=True))