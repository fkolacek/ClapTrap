#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Message(object):

  channel = None
  date = None
  nick = None
  message = None

  def __init__(self, raw):
    try:
      match = re.search('^.+\/([^\/]+)\/out\: ([0-9\-]+ [0-9\:]+) <(.+)> (.*)$', raw)

      self.channel, self.date, self.nick, self.message = match.groups()
    except AttributeError:
      print "[!] Invalid message: %s" % raw

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


