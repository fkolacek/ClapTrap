#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pprint import pprint

class Users(object):

  def __init__(self):
    self._users = []

  def addUser(self, user):
    if not self.isUser(user):
      self._users.append(user)

  def delUser(self, user):
    if self.isUser(user):
      self._users.remove(user)

    if len(self._users) == 0:
      self._users = []

  def isUser(self, user):
    return user in self._users

class Controller(object):

  def __init__(self, bot):
    self._nick = bot.config['nick']
    self._channels = bot.config['channels']

    self._users = {}
    for channel in self._channels:
      self._users[channel] = Users()

    self._regexps = {
      # [*] Processing message c:#test n:fkolacek m:(~fkolacek@example.com) has joined #test
      'join': '^(.+) has joined (.+)$',
      # [*] Processing message c:#test n:fkolacek m:(~fkolacek@example.com) has left #test
      'part': '^(.+) has left (.+)$',
      # [*] Processing message c:#test n:fkolacek m:kicked ClapTrap ("ClapTrap")
      'kick': '^kicked ([^ ]+) (.*)$',
      #[*] Processing message c:irc.devel.redhat.com n:fkolacek m:changed nick to fkolacek-brb
      'nick': '^changed nick to (.+)$',
      # [*] Processing message c:irc.devel.redhat.com n:fkolacek m:(~fkolacek@example.com) has quit "Client Quit"
      'quit': '^(.+) has quit (.+)$',
      # [*] Processing message c:#test n:fkolacek m:changed mode/#test -> +o ClapTrap
      'mode': '^changed mode',
    }

  def processMessage(self, bot, message):

    if message.isSystem():
      for action, regexp in self._regexps.iteritems():
        match = re.search(regexp, message.message)

        if match:
          if action == 'join':
            self._users[message.channel].addUser(message.nick)
          elif action == 'part':
            self._users[message.channel].delUser(message.nick)
          elif action == 'kick':
            kicked, reason = match.groups()
            self._users[message.channel].delUser(kicked)
          elif action == 'nick':
            nick = match.groups(1)[0]
            for channel in self._channels:
              if self._users[channel].isUser(message.nick):
                self._users[channel].delUser(message.nick)
                self._users[channel].addUser(nick)
          elif action == 'quit':
            for channel in self._channels:
              self._users[channel].delUser(message.nick)
          else:
            # Message is not yet supported!
            pass

          for channel in self._channels:
            print "[*] Users on %s: %s" % (channel, ','.join(self._users[channel]._users))
        else:
          # Message didn't match any known regexp
          pass
    elif message.isValid():
      pass
    # Message is invalid - not known
    else:
      ####
      #### This should ne moved somewhere else in the future!
      ####

      # 2017-01-01 00= #test :@FLC user1 user2
      match = re.search("^.* = (#[^ ]+) (.+)$", message.raw)

      if match:
        channel, users = match.groups()

        for part in [ '@', '+', bot.config['nick']]:
            users = users.replace(part, '')

        for user in users.strip().split(' '):
          self._users[channel.lower()].addUser(user)
