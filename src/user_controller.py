from common import *

import cgi, sessions

from paste_model import Paste
from userdata_model import UserData

from google.appengine.ext.webapp import template

class Profile(sessions.PersistentRequestHandler):
	def get(self, usercode=None):
		self.init_session()
		if self.do_redirect(): return
		
		if usercode is None:
			usercode = self.get_key('usercode')
			if usercode is None:
				self.redirect('/')
				return
		elif usercode[0] == '/':
			usercode = usercode[1:]
		
		your_profile = (usercode == self.get_key('usercode'))

		if your_profile:
			pastes = Paste.get_all_by_usercode(usercode)
		else:
			pastes = Paste.get_public_by_usercode(usercode)
		

class Settings(sessions.PersistentRequestHandler):
	  def get(self):
		self.init_session()
		if self.do_redirect(): return

		if 'usercode' not in self.session:
			#print self.session
			self.redirect('/')
			return
		
		self.template_values.update({
			'apikey': UserData.get_apikey_by_code(self.session['usercode'])
		})
		
		path = get_template_path('settings.html')
		self.response.out.write(template.render(path, self.template_values, debug=True))