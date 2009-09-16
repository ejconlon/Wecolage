from common import *

from google.appengine.api import users
from userdata_model import UserData
from appengine_utilities import sessions

def reset_redirect(self, session):
	if 'redirect' in session:
		r = session['redirect']
		session.delete_item('redirect')
		self.redirect(r)
		return True
	else:
		return False

def get_key(session, key):
	if key in session:
		return session[key]
	else:
		return None

def get_user(session):
	return get_key(session, 'user')
def get_usercode(session):
	return get_key(session, 'usercode')
		
def reset_flash(session):
	if 'flash' in session:
		flash = session['flash']
		session.delete_item('flash')
		return flash
	else:
		return None
	
def get_session(request_uri='/'):
	session = sessions.Session()
	user = users.get_current_user()
	if 'user' in session and session['user'] != user:
		session.delete()
		session = sessions.Session()
	if not (user is None):
		session['user'] = user
	session['login_url'] = users.create_login_url(request_uri)
	session['logout_url'] = users.create_logout_url(request_uri)
	if 'got_userdata' in session and session['got_userdata']:
		return session
	return load_userdata_into_session(session)
	
def load_userdata_into_session(session):
	if 'user' in session:
		user = session['user']
		# is user in the userdata table? else make it and go to the settings page
		userdata = UserData.get_by_user(user)
		if userdata is None:
			userdata = UserData()
			userdata.code = new_code(usercodelen)
			userdata.user = user
			userdata.email = user.email()
			userdata.nickname = user.nickname()
			userdata.api_key = new_code(apikeylen)
			userdata.pastes_hidden_by_default = False
			userdata.put()
			session['redirect'] = '/settings/'+userdata.code
			session['flash'] = 'Maybe you\'d like to change your default settings. If not, <a href="/">paste away</a>.'
		session['usercode'] = userdata.code
		session['nickname'] = userdata.nickname
		session['email'] = userdata.email
		session['pastes_hidden_by_default'] = userdata.pastes_hidden_by_default
		session['got_userdata'] = True
	else:
		#session['user'] = None
		session['nickname'] = 'Anonymous'
		#session['email'] = None
		session['pastes_hidden_by_default'] = False
		session['got_userdata'] = False
	return session
	
def destroy_session(session):
	session.delete()