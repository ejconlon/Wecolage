from common import *

from google.appengine.ext import db

class FriendRequest(db.Model):
	my_code = db.StringProperty()
	their_code = db.StringProperty()
	date_requested = db.DateTimeProperty(auto_now_add=True)
	
	@staticmethod
	def make_request(code1, code2):
		r = FriendRequest()
		r.my_code = code1
		r.their_code = code2
		r.put()
	
	@staticmethod
	def unmake_request(code1, code2):
		request = FriendRequest.gql("WHERE my_code=:code1 AND their_code=:code2",
										code1=code1, code2=code2)
		db.delete(request)

	@staticmethod
	def get_who_user_requested_to_follow(code):
		return FriendRequest.gql("WHERE my_code=:code", code=code)
	
	@staticmethod
	def get_who_requested_to_follow_user(code):
		return FriendRequest.gql("WHERE their_code=:code", code=code)
	
	@staticmethod
	def already_present(code1, code2):
		return FriendRequest.gql("WHERE my_code=:code1 AND their_code=:code2",
										code1=code1, code2=code2).count() > 0
	
	@staticmethod
	def get_number_of_requests(code):
		return FriendRequest.get_who_requested_to_follow_user(code).count()