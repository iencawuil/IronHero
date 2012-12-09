import cgi
import datetime

from google.appengine.ext import db
from google.appengine.api import users



class Move(db.Model):
	name = db.StringProperty()

class Activity(db.Model):
#	user = db.UserProperty()
	move = db.ReferenceProperty(Move)
	reps = db.IntegerProperty()
	weight = db.IntegerProperty()
