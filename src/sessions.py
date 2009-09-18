from common import *

from google.appengine.api import users
from userdata_model import UserData
from codes_model import Usercode, Apikey
from friendrequest_model import FriendRequest
from appengine_utilities import sessions

from google.appengine.ext import webapp

class PersistentRequestHandler(webapp.RequestHandler):
	#def __init__(self):
	#	webapp.RequestHandler.__init__(self)
	
	def init_session(self):
		self.session = PersistentRequestHandler.get_session(self.request.uri)
		if 'redirect' in self.session: 
			return
		if 'current' in self.session:
			self.session['previous'] = self.session['current']
		else:
			self.session.delete_item('previous')
		self.session['current'] = self.request.uri
			
		self.template_values = {
			'session': self.session,
			'flash': self.get_flash()
		}
		
	def do_redirect(self):
		if 'redirect' in self.session:
			r = self.session['redirect']
			self.session['redirect'] = '/404'
			self.session.delete_item('redirect')
			self.redirect(r)
			return True
		else:
			return False

	def get_flash(self):
		if 'flash' in self.session:
			flash = self.session['flash']
			self.session['flash'] = ''
			self.session.delete_item('flash')
			return flash
		else:
			return None
	
	def get_key(self, key):
		if key in self.session: return self.session[key]
		else: return None
	
	@staticmethod
	def get_session(request_uri):
		session = sessions.Session()
		user = users.get_current_user()
		session['login_url'] = users.create_login_url(request_uri)
		session['logout_url'] = users.create_logout_url(request_uri)
		if 'user' in session and session['user'] != user:
			session.delete()
			session = sessions.Session()
		if user is None:
			return PersistentRequestHandler.load_userdata_into_session(session)
		else:
			session['user'] = user
			if 'got_userdata' in session and session['got_userdata']:
				session['num_friend_requests'] = FriendRequest.get_number_of_requests(session['usercode'])
				return session
			return PersistentRequestHandler.load_userdata_into_session(session)
	
	@staticmethod
	def load_userdata_into_session(session):
		if 'user' in session:
			user = session['user']
		#	 is user in the userdata table? else make it and go to the settings page
			userdata = UserData.get_by_user(user)
			if userdata is None:
				userdata = UserData()
				userdata.usercode = Usercode().new_code()
				userdata.user = user
				userdata.email = user.email()
				userdata.nickname = user.nickname()
				userdata.apikey = Apikey().new_code()
				userdata.pastes_hidden_by_default = False
				userdata.put()
				session['redirect'] = '/settings'
				session['flash'] = 'Maybe you\'d like to change your default settings. If not, <a href="/">paste away</a>.'
			session['usercode'] = userdata.usercode
			session['nickname'] = userdata.nickname
			session['email'] = userdata.email
			session['pastes_hidden_by_default'] = userdata.pastes_hidden_by_default
			session['friends_hidden_by_default'] = userdata.friends_hidden_by_default
			session['num_friend_requests'] = FriendRequest.get_number_of_requests(userdata.usercode)
			session['got_userdata'] = True
		else:
			session['nickname'] = 'Anonymous'
			session['pastes_hidden_by_default'] = False
			session['friends_hidden_by_default'] = False
			session['num_friend_requests'] = 0
			session['got_userdata'] = False
		return session
		
	def restore_previous(self, flash=None):
		if 'previous' in self.session:
			if flash:
				self.session['flash'] = flash
			previous = self.session['previous']
			self.session.delete_item('previous')
			self.session.delete_item('current')
			self.redirect(previous)
			return True
		else:
			return False
	