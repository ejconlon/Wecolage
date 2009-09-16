from common import *

import cgi, sessions

from paste_model import Paste

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Filer(webapp.RequestHandler):
	def get(self, args):
		session = sessions.get_session(self.request.uri)
		if sessions.reset_redirect(self, session): return
		flash = sessions.reset_flash(session)
		
		args = cgi.escape(args).split('/')
		if len(args) > 2:
			logger.error("Bad filer args: "+str(args))
			self.redirect('/404')
			return
		code = args[0]
		filename = None
		if len(args) == 2:
			filename = args[1]
			
		paste = Paste.get_by_code(code)
		if paste is None:
			logger.error("PASTE "+code+" NOT FOUND")
			self.redirect('/404')
			return
		
		if filename is None:
			filename = make_filename(paste.name)+formatting.formats[paste.format]['extension']
			self.redirect('/file/'+code+'/'+filename)
			return
		
		self.response.headers['Content-type'] = formatting.formats[paste.format]['mimetype']
		path = get_template_path('file_out')
		self.response.out.write(template.render(path, {'content':paste.content}, debug=True))
