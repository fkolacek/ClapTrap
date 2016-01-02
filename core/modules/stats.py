#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

class Stats(object):

  meta = {
    'name': "Stats",
    'description': "Module provides basic server/channel statistics",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "1.0",
    'triggers': {
      '^!top ?': "callTop",
      '^[^!].*': "callRecord",
      '^!seen': "callSeen",
      '^!last': "callLast",
      '^!uptime': "callUptime"
    }
  }

  def __init__(self, bot):
    bot.database.execute("CREATE TABLE IF NOT EXISTS Stats_messages (Id INTEGER PRIMARY KEY AUTOINCREMENT, Channel TEXT, Nick TEXT, Count INT, Date TEXT, Message TEXT)")

    self._uptime = time.time()

  def callTop(self, bot, message):
    cmd = message.cmd()

    if cmd and cmd == "!top":
      if message.isPrivate():
        bot.addReply(message.channel, "This command is not supposed to be used via query")
        return

      args = message.args()

      # !top
      if len(args) == 0:
        data = bot.database.execute("SELECT Nick, Count FROM Stats_messages WHERE Channel = ? ORDER BY Count DESC LIMIT 5",(message.channel,))

        score = []
        for row in data:
          score.append("%s(%s)" % (row[0], row[1]))

        if len(score) == 0:
          bot.addReply(message.channel, "There are no spammers on this channel")
        else:
          bot.addReply(message.channel, "Top spammers: %s" % ", ".join(score))
      # !top [nick]
      elif len(args) == 1:
        exists = bot.database.fetchone("SELECT Nick FROM Stats_messages WHERE Nick = ? AND Channel = ? LIMIT 1", (args[0], message.channel, ))

        if not exists:
          bot.addReply(message.channel, "No message from %s recorded on this channel" % args[0])
        else:
          data = bot.database.fetchone("SELECT Count FROM Stats_messages WHERE Nick = ? AND Channel = ? LIMIT 1", (args[0], message.channel, ))
          bot.addReply(message.channel, "User %s has sent %d messages to this channel" % (args[0], data[0]))
      # Invalid usage
      else:
        bot.addReply(message.channel, "Usage: !top [nick]")

  def callRecord(self, bot, message):
    if not message.isPrivate():
      t = time.strftime('%Y-%m-%d %H:%M:%S')

      exists = bot.database.fetchone("SELECT Nick FROM Stats_messages WHERE Nick = ? AND Channel = ? LIMIT 1", (message.nick, message.channel, ))

      if not exists:
        bot.database.execute("INSERT INTO Stats_messages (Nick, Channel, Date, Count, Message) VALUES (?, ?, ?, 1, ?)", (message.nick, message.channel, t, message.message, ))
      else:
        bot.database.execute("UPDATE Stats_messages SET Count=Count+1, Date=?, Message=? WHERE Nick = ? AND Channel = ?", (t, message.message, message.nick, message.channel, ))

  def callSeen(self, bot, message):
    cmd = message.cmd()

    if cmd and cmd == "!seen":
      args = message.args()

      # !seen [nick]
      if len(args) == 1:
        exists = bot.database.fetchone("SELECT Nick FROM Stats_messages WHERE Nick = ?", (args[0], ))

        if exists:
          data = bot.database.fetchone("SELECT Channel, Date, Message FROM Stats_messages WHERE Nick = ? ORDER BY Date DESC LIMIT 1", (args[0], ))
          bot.addReply(message.channel, "User %s was last seen %s on %s" % (args[0], data[1], data[0]))
        else:
          bot.addReply(message.channel, "I haven't seen user %s on this server" % args[0])
      # Invalid usage
      else:
        bot.addReply(message.channel, "Usage: !seen [nick]")
  
  def callLast(self, bot, message):
    cmd = message.cmd()

    if cmd and cmd == "!last":
      args = message.args()

      if len(args) == 0:
        args.append(message.nick)

      # !last [nick]
      if len(args) == 1:
        exists = bot.database.fetchone("SELECT Nick FROM Stats_messages WHERE Nick = ?", (args[0], ))

        if exists:
          data = bot.database.fetchone("SELECT Date, Message, Channel FROM Stats_messages WHERE Nick = ? ORDER BY Date DESC LIMIT 1", (args[0], ))
          bot.addReply(message.channel, "Last message from user %s sended %s to %s was: %s" % (args[0], data[0], data[2], data[1]))
        else:
          bot.addReply(message.channel, "I haven't seen user %s on this server" % args[0])
      # Invalid usage
      else:
        bot.addReply(message.channel, "Usage: !last [nick]")

  def callUptime(self, bot, message):
    cmd = message.cmd()

    if cmd and cmd == "!uptime":
      delta = time.time() - self._uptime
      
      d = datetime(1,1,1) + timedelta(seconds=delta)

      bot.addReply(message.channel, "Uptime is %d days, %d hours, %d minutes and %d seconds" % (d.day-1, d.hour, d.minute, d.second))
