from common import *

from google.appengine.ext import db

class UserData(db.Model):
	user = db.UserProperty()
	usercode = db.StringProperty()
	apikey = db.StringProperty()
	nickname = db.StringProperty()
	email = db.EmailProperty()
	pastes_hidden_by_default = db.BooleanProperty(default=False)
	friends_hidden_by_default = db.BooleanProperty(default=False)
	
	@staticmethod
	def get_by_code(code):
		udatas = UserData.gql("WHERE usercode=:code", code=code)
		if udatas.count() != 1:
			return None
		else:
			return udatas.fetch(1)[0]	

	@staticmethod
	def get_by_codes(codes):
		return UserData.gql("WHERE usercode IN :codes", codes=codes)

	@staticmethod
	def get_by_user(user):
		udatas = UserData.gql("WHERE user=:user", user=user)
		if udatas.count() != 1:
			return None
		else:
			return udatas.fetch(1)[0]
			
	@staticmethod
	def get_apikey_by_code(code):
		udata = UserData.get_by_code(code)
		if not (udata is None):
			return udata.apikey
		else:
			return None
	
	@staticmethod
	def check_apikey(code, key):
		return (key == UserData.get_apikey_by_code(key))