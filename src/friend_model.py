from common import *

from google.appengine.ext import db

class Friend(db.Model):
	my_code = db.StringProperty()
	their_code = db.StringProperty()
	date_friended = db.DateTimeProperty(auto_now_add=True)
	
	@staticmethod
	def make_friends(code1, code2):
		f = Friend()
		f.my_code = code1
		f.their_code = code2
		f.put()
	
	@staticmethod
	def unmake_friends(code1, code2):
		friend = Friend.gql("WHERE (my_code=:code1 AND their_code=:code2)",
										code1=code1, code2=code2)
		db.delete(friend)

	@staticmethod
	def get_who_i_follow(code):
		return Friend.gql("WHERE my_code=:code", code=code)
			
	@staticmethod
	def get_who_follows_user(code):
		return Friend.gql("WHERE their_code=:code", code=code)

	@staticmethod
	def already_present(code1, code2):
		return Friend.gql("WHERE (my_code=:code1 AND their_code=:code2)",
										code1=code1, code2=code2).count() > 0
