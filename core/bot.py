#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pkgutil
import importlib
import time
import re

from database import Database
from watcher import Watcher
from message import Message
from controller import Controller
from pprint import pprint

class Bot(object):

  #
  def __init__(self, args):

    self.config = {
      'ircdir':   args[1],
      'server':   args[2],
      'nick':     args[3],
      'workdir':  os.path.dirname(os.path.abspath(__file__)),
    }

    self.database = None

    self._modulesPath = None
    self._modulesList = []

    self._triggers = []
    self._replies = []

    try:
      self._initDatabase()
      self._initModules()

      self._controller = Controller(self)
      self._watcher = Watcher(self.config['ircdir'], self._callback, ['out'])
    except:
      e = sys.exc_info()
      print "[!] Uncaught exception: %s - %s" % (e[0], e[1])
      sys.exit(1)

  #
  def _initDatabase(self):
    print "[*] Initializing database.."
    self.database = Database("%s/%s.db" % (self.config['ircdir'], self.config['server']))

  #
  def _initModules(self):
    print "[*] Initializing modules.."

    self._triggers = []

    self._modulesPath = "%s/modules" % self.config['workdir']

    self._modulesList = pkgutil.iter_modules(path=[self._modulesPath])

    for loader, modName, ispkg in self._modulesList:
      self._loadModule(modName)

  #
  def _loadModule(self, modName):
    if modName not in sys.modules:
      modTitle = modName.title()

      print "[*] Loading module %s [%s/%s]" % (modTitle, self._modulesPath, modName)

      # Import module
      mod = __import__("modules.%s" % modName, fromlist=[modTitle])

      # Get class
      cls = getattr(mod, modTitle)

      # Create object
      obj = cls(self)

      if not hasattr(obj, 'meta'):
        print "[!] No meta section in module %s, skipping" % modTitle
        return

      if 'triggers' not in obj.meta:
        print "[!] No triggers in module %s, skipping" % modTitle
        return

      if 'usage' not in obj.meta:
        print "[?] No usage section in module %s, module won't be listed in help" % modTitle

      for trigger, callback in obj.meta['triggers'].iteritems():

        valid =  True
        try:
          re.compile(trigger)
        except re.error:
          valid = False

        if not valid:
          print "[!] Trigger %s is not valid regex, skipping" % trigger
          continue

        if callable(getattr(obj, callback, None)):
          print "[*] Trigger %s registered for callback %s.%s" % (trigger, modTitle, callback)
          t = {
            'module':   modTitle,
            'trigger':  trigger,
            'object':   obj,
            'callback': callback
          }

          self._triggers.append(t)
        else:
          print "[!] Callback %s.%s is not callable, skipping" % (modTitle, callback)

  #
  def _callback(self, filename, lines):
    for line in lines:
      message = Message("%s: %s" % (filename, line.strip()))

      if message.nick == self.config['nick']:
        continue

      if message.isValid():
        print "[*] Processing message c:%s n:%s m:%s" % (message.channel, message.nick, message.message)

        for trigger in self._triggers:
          if re.search(trigger['trigger'], message.message):
            print "[*] Processing callback %s.%s" % (trigger['module'], trigger['callback'])
            try:
              getattr(trigger['object'], trigger['callback'])(self, message)
            except:
              e = sys.exc_info()
              print "[!] Uncaught exception: %s - %s" % (e[0], e[1])

  #
  def addReply(self, channel, message):
    reply = {
      'channel': channel,
      'message': message
    }

    self._replies.insert(0, reply)

  #
  def sendReply(self, reply):
    outputFile = "%s/%s/%s/in" % (self.config['ircdir'], self.config['server'], reply['channel'])

    if os.path.exists(outputFile):
      print "[*] Sending reply %s to %s" % (reply['message'], reply['channel'])
      with open("%s" % outputFile, "a") as f: f.write("%s\n" % reply['message'])
    else:
      print "[!] Output file does not exist: %s" % outputFile

  #
  def run(self):
    print "[*] Starting main loop.."

    while True:
      self._watcher.loop(blocking=False)

      if len(self._replies) > 0:
        reply = self._replies.pop()

        self.sendReply(reply)

      time.sleep(0.1)
