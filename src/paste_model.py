from common import *

import random, datetime

from google.appengine.ext import db

class Paste(db.Model):
	owner = db.UserProperty()
	owner_code = db.StringProperty()
	name = db.StringProperty()
	content = db.TextProperty()
	parsed_content = db.TextProperty()
	parent_diff = db.TextProperty()
	parsed_parent_diff = db.TextProperty()
	format = db.StringProperty()
	date_created = db.DateTimeProperty(auto_now_add=True)
	password_hash = db.StringProperty()
	hidden = db.BooleanProperty(default=False)
	code = db.StringProperty()
	parent_code = db.StringProperty()
	ancestor_code = db.StringProperty()
	marked_for_deletion = db.BooleanProperty(default=False)
	
	def check_password(self, password):
		if password is None:
			return (self.password_hash is None)
		else:
			test_hash = sha1(self.code + password + self.code)
			return (self.password_hash == test_hash)
	
	def save_new(self, password=None):
		while True:
			code = "".join((random.choice(codechars) for i in xrange(codelen)))
			pastes_with_code = Paste.gql("WHERE code=:code", code=code)
			if (pastes_with_code.count() == 0):
				break
		self.code = code
		if not (password is None) and len(password) > 0:
			self.password_hash = sha1(code + password + code)
		self.put()

	def start_fork(self, user=None):
		paste = Paste()
		paste.owner = user
		paste.name = self.name
		paste.content = self.content
		paste.parsed_content = self.parsed_content
		paste.format = self.format
		paste.date_created = datetime.datetime.now()
		paste.parent_code = self.code
		if self.ancestor_code is None:
			paste.ancestor_code = self.code
		else:
			paste.ancestor_code = self.ancestor_code
		return paste
	
	def get_url(self):
		return '/read/'+self.code

	@staticmethod
	def get_by_code(code):
		pastes = Paste.gql("WHERE code=:code", code=code)
		if pastes.count() != 1:
			return None
		else:
			return pastes.fetch(1)[0]
