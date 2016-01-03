#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Logger(object):

  meta = {
    'name': "Logger",
    'description': "Base module for logging message",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "1.0",
    'triggers': {
      '.*': "callLog"
    }
  }

  def __init__(self, bot):
    pass

  def callLog(self, bot, message):
    if not os.path.isdir("%s/logs" % bot.config['ircdir']):
      os.mkdir("%s/logs" % bot.config['ircdir'], 0755)

    filename = "%s/logs/%s.log" % (bot.config['ircdir'], message.channel)
    
    if message.isSystem():
      with open("%s" % filename, "a") as f: f.write("%s %s %s\n" % (message.date, message.nick, message.message))
    else:
      with open("%s" % filename, "a") as f: f.write("%s <%s> %s\n" % (message.date, message.nick, message.message))

