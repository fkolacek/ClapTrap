#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SingleChannel for now!

import time
from pprint import pprint

class Custom(object):

  meta = {
    'name': "Custom",
    'description': "Custom functions",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "1.0",
    'triggers': {
      '^!coffee': "whatAboutCoffee",
      '^(y|n)$': "recordAnswers",
    },
    'usage': [
      "!coffee - Asks everyone on channel if they want coffee"
    ]
  }

  def __init__(self, bot):
    self._last = 0
    self._requester = None
    self._channel = None
    self._mode = False
    self._answers = {}
    self._drinkers = 0

  def whatAboutCoffee(self, bot, message):
    if message.isSystem():
      return

    cmd = message.cmd()

    if cmd and cmd == "!coffee":
      if time.time() - self._last < 15:
        bot.addReply(message.channel, "%s: please wait 15 seconds before asking for coffee again (you should also work you know)!" % message.nick)
        return

      users = list(bot._controller._users[message.channel]._users)

      for u in ['CHANSERV', 'USERSERV', message.nick]:
        if u in users:
          users.remove(u)

      if len(users) > 0:
        self._requester = message.nick
        self._channel = message.channel
        self._mode = True
        self._answers = {}
        self._drinkers = len(users)
        self._answers[message.nick] = True
        bot.addReply(message.channel, "Coffee time(y/n)? %s" % ','.join(users))

        self._last = time.time()
      else:
        bot.addReply(message.channel, "Forever alone huh? Go and make coffee for yourself.. just don't bother me!")

  def recordAnswers(self, bot, message):
    if message.isSystem():
      return

    if self._mode:
      if message.message == 'y':
        print "[*] Got y from %s" % message.nick
        self._answers[message.nick] = True
      elif message.message == 'n':
        print "[*] Got n from %s" % message.nick
        self._answers[message.nick] = False

      self.getResults(bot)

  def getResults(self, bot):
    if len(self._answers) == self._drinkers:
      drinkers = []
      for user,answer in self._answers.iteritems():
        if answer:
          drinkers.append(user)

      if len(drinkers) == 0:
        bot.addReply(self._channel, "%s: No one wants to have coffee with you!" % (self._requester))
      elif len(drinkers) == 1:
        bot.addReply(self._channel, "%s: Only %s wants to have coffee with you." % (self._requester, ','.join(drinkers)))
      else:
        bot.addReply(self._channel, "%s: Make coffee for %d people(%s)" % (self._requester, len(drinkers), ','.join(drinkers)))

      self._mode = False

  def tick(self, bot):
    if self._mode:
      if time.time() - self._last > 60:

        bot.addReply(self._channel, "I waited long enough.. let's close it.")
        self._drinkers = len(self._answers)
        self.getResults(bot)
