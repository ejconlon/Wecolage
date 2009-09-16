from common import *

from google.appengine.ext import db

class UserData(db.Model):
	user = db.UserProperty()
	code = db.StringProperty()
	api_key = db.StringProperty()
	nickname = db.StringProperty()
	email = db.EmailProperty()
	pastes_hidden_by_default = db.BooleanProperty(default=False)
	
	@staticmethod
	def get_by_code(code):
		udatas = UserData.gql("WHERE code=:code", code=code)
		if udatas.count() != 1:
			return None
		else:
			return udatas.fetch(1)[0]	

	@staticmethod
	def get_by_user(user):
		udatas = UserData.gql("WHERE user=:user", user=user)
		if udatas.count() != 1:
			return None
		else:
			return udatas.fetch(1)[0]
			
	@staticmethod
	def get_api_key_by_code(code):
		udata = UserData.get_by_code(code)
		if not (udata is None):
			return udata.api_key
		else:
			return None
	
	@staticmethod
	def check_api_key(code, key):
		return (key == UserData.get_api_key_by_code(key))