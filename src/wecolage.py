# wecolage.py - Eric Conlon - Sept 2009

import sys, os
sys.path.append(os.path.dirname(__file__))

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import home_controller
import paster_controller
import reader_controller
import forker_controller
import filer_controller
import settings_controller
		
application = webapp.WSGIApplication(
	[
		('/', 				home_controller.Home),
		('/paste/?', 		paster_controller.Paster),
		('/read/(.+)', 		reader_controller.Reader),
		('/fork/(.+)', 		forker_controller.Forker),
		('/fork/?', 		forker_controller.Forker),
		('/file/(.+)', 		filer_controller.Filer),
		('/settings/(.+)', 	settings_controller.Settings),
	],
	debug = True
)

def main():
	run_wsgi_app(application)
	
if __name__ == "__main__":
	main()