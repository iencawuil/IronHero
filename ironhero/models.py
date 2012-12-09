import cgi
import datetime

from google.appengine.ext import db
from google.appengine.api import users


class Move(db.Model):
	name = db.StringProperty()
	equipment = db.StringProperty()
	# longName = db.StringProperty()
	# shortName = db.StringProperty()
	# power = db.FloatProperty()
	# minWeight = db.IntegerProperty()
	# maxWeight = db.IntegerProperty()

	# def serialize(self):
	# 	d = {'name' : self.name, 'longName' : self.longName, 'shortName' : self.shortName, 'power' : self.power, 'minWeight' : self.minWeight, 'maxWeight': self.maxWeight}
	# 	return d		

	def serialize(self):
		d = {'name' : self.name, 'equipment' : self.equipment, 'key' : str(self.key())}
		return d		




####THIS IS GOING IN LATRO IN LIFE####
class Activity(db.Model):	
	move = db.ReferenceProperty(Move)
	reps = db.IntegerProperty()
	weight = db.IntegerProperty()


class Round(db.Model):
	activities = db.ReferenceProperty(Activity);


class Workout(db.Model):
	user = db.UserProperty()
	rounds = db.ReferenceProperty(Round)
	name = db.StringProperty()