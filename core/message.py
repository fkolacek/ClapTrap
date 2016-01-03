#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Message(object):

  def __init__(self, raw):
    self.channel = None
    self.date = None
    self.nick = None
    self.message = None
    self.system = False

    regularMessage = '^.+\/([^\/]+)\/out\: ([0-9\-]+ [0-9\:]+) <(.+)> (.*)$'
    systemMessage = '^.+\/([^\/]+)\/out\: ([0-9\-]+ [0-9\:]+) \-\!\- ([^\( ]+) ?(.*)$'

    regularMatch = re.search(regularMessage, raw)
    systemMatch = re.search(systemMessage, raw)

    if regularMatch:
      self.channel, self.date, self.nick, self.message = regularMatch.groups()
    elif systemMatch:
      self.channel, self.date, self.nick, self.message = systemMatch.groups()
      self.system = True
    else:
      print "[!] Invalid message: %s" % raw

  def isSystem(self):
    return self.system

  def isPrivate(self):
    return not self.channel.startswith("#")

  def isValid(self):
    return self.channel and self.date and self.nick and self.message

  def cmd(self):
    parts = self.message.split(' ')

    if len(parts) > 0:
      return parts[0]
    else:
      return None

  def args(self):
    parts = self.message.split(' ')

    if len(parts) > 1:
      parts.pop(0)
      return parts
    else:
      return []


