#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import pickle
from urllib import FancyURLopener
import urllib
from datetime import datetime
import logging
import os
import models
import simplejson


class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'views/main.html')
        self.response.out.write(template.render(path, template_values))

class NewMoveHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'views/new_move.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        logging.info("Jason Jason Jason")
        logging.info(self.request)
        name = self.request.get('move_name')
        equipment = self.request.get('equipment')
        logging.info(len(name))
        if len(name) > 0:
            logging.info("Creating move")
            # name[0] = name[0].upper() ##find proper function for this
            move = models.Move(key_name=name,name=name, equipment=equipment)
            move.put()
            logging.info(move)
        else:
            logging.info("ruhruo")
        self.redirect('/moves')

        
class NewActivityHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        moves = models.Move.all();
        template_values['moves'] = moves
        path = os.path.join(os.path.dirname(__file__), 'views/new_activity.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        moveKey = self.request.get('move_name')
        move = models.Move.get(moveKey)
        self.response.out.write(move.name)

class allMovesHandler(webapp.RequestHandler):
    def get(self):
        moves = models.Move.all()
        template_values = {'moves':moves}
        path = os.path.join(os.path.dirname(__file__), 'views/all_moves.html')
        self.response.out.write(template.render(path, template_values))

class AllActivitiesHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'views/all_activities.html')
        self.response.out.write(template.render(path, template_values))
        
class NewWorkoutHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'views/new_workout.html')
        self.response.out.write(template.render(path, template_values))

class RPCHandler(webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = RPCMethods()

    def get(self):
        func = None

        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403) # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        args = []
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                logging.debug(val)
                args.append(simplejson.loads(val))
            else:
                break
        args = tuple(args)
        result = func(*args)
        logging.debug(result)
        self.response.out.write(simplejson.dumps(result))

class RPCMethods:
    """ Defines the methods that can be RPCed.
    NOTE: Do not allow remote callers access to private/protected "_*" methods.
    """
    def Add(self, *args):
        # The JSON encoding may have encoded integers as strings.
        # Be sure to convert args to any mandatory type(s).
        ints = [int(arg) for arg in args]
        return sum(ints)

    def allMoves(self,*args):
        ##ignore args
        moves = models.Move.all();
        allMoves = [{'name': m.name} for m in moves]
        # allMoves = moves.fetch(moves.count())
        return allMoves
    def moveDetails(self,*args):
        key = args[0]
        logging.debug(key)
        move = models.Move.get(key)
        return move.serialize()

        
        
                
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
    ('/new_move', NewMoveHandler),
    ('/new_activity', NewActivityHandler),
    ('/rpc',RPCHandler),
    ('/all_activities',AllActivitiesHandler),
    ('/new_workout',NewWorkoutHandler),
    ('/moves', allMovesHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
