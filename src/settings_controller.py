from common import *

import cgi, sessions

from paste_model import Paste
from userdata_model import UserData

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Settings(webapp.RequestHandler):
	  def get(self, usercode):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
			
		usercode = cgi.escape(usercode)
		if 'usercode' not in session or usercode != session['usercode']:
			self.redirect('/')
			return
		elif session['usercode'] is None:
			self.redirect(session['login_url'])
			return
			
		template_values = {
			'session': session,
			'flash': flash,
			'api_key': UserData.get_api_key_by_code(session['usercode'])
		}
		
		path = get_template_path('settings.html')
		self.response.out.write(template.render(path, template_values, debug=True))