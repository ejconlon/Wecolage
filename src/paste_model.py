from common import *

import random, datetime

from codes_model import Pastecode

from google.appengine.ext import db

class Paste(db.Model):
	pastecode = db.StringProperty()
	usercode = db.StringProperty()
	name = db.StringProperty()
	description = db.TextProperty()
	content = db.TextProperty()
	parsed_content = db.TextProperty()
	parent_diff = db.TextProperty()
	parsed_parent_diff = db.TextProperty()
	format = db.StringProperty()
	date_created = db.DateTimeProperty(auto_now_add=True)
	password_hash = db.StringProperty()
	hidden = db.BooleanProperty(default=False)
	parent_code = db.StringProperty()
	ancestor_code = db.StringProperty()
	marked_for_deletion = db.BooleanProperty(default=False)
	
	def check_password(self, password):
		if password is None or len(password)==0:
			return (self.password_hash is None)
		else:
			test_hash = sha1(self.pastecode + password + self.pastecode)
			return (self.password_hash == test_hash)
	
	def save_new(self, password=None):
		self.pastecode = Pastecode().new_code()
		if not (password is None) and len(password) > 0:
			self.password_hash = sha1(pastecode + password + pastecode)
		self.put()

	def start_fork(self, usercode=None):
		paste = Paste()
		paste.usercode = usercode
		paste.name = self.name
		paste.content = self.content
		paste.parsed_content = self.parsed_content
		paste.format = self.format
		paste.date_created = datetime.datetime.now()
		paste.parent_code = self.pastecode
		if self.ancestor_code is None:
			paste.ancestor_code = self.pastecode
		else:
			paste.ancestor_code = self.ancestor_code
		return paste
	
	def get_url(self):
		return '/paste/'+self.pastecode

	@staticmethod
	def get_by_code(pastecode):
		pastes = Paste.gql("WHERE pastecode=:pastecode", pastecode=pastecode)
		if pastes.count() != 1:
			return None
		else:
			return pastes.fetch(1)[0]
			
	@staticmethod
	def get_all_by_usercode(usercode):
		return Paste.gql("WHERE usercode=:usercode ORDER BY date_created DESC", usercode=usercode)
		
	@staticmethod
	def get_public_by_usercode(usercode):
			return Paste.gql("WHERE usercode=:usercode AND hidden=False ORDER BY date_created DESC", usercode=usercode)
