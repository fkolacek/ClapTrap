#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import re

class Mail(object):

  meta = {
    'name': "Mail",
    'description': "",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "0.1",
    'triggers': {
      '^!tell': "callTell",
      '.*': "callWatch"
    },
    'usage': [
      "!tell [nick] [message] - "
    ]
  }

  def __init__(self, bot):
    bot.database.execute("CREATE TABLE IF NOT EXISTS Mail_messages (Id INTEGER PRIMARY KEY AUTOINCREMENT, Channel TEXT, Nick TEXT, Sender Text, Date TEXT, Message TEXT, Active INT)")

    self._regexps = {
      'join': '\-\!\- ([^\(]+)\(.+ has joined ([^ ]+)',
      'nick': '\-\!\- ([^ ]+) changed nick to ([^ ]+)'
    }

  def callTell(self, bot, message):
    if message.isSystem():
      return

    cmd = message.cmd()

    if cmd and cmd == "!tell":
      if message.isPrivate():
        bot.addReply(message.channel, "This command is not supposed to be used via query")
        return

      args = message.args()

      if len(args) >= 2:
        nick = args.pop(0)
        msg = ' '.join(args)
        t = time.strftime('%Y-%m-%d %H:%M')

        bot.database.execute("INSERT INTO Mail_messages (Channel, Nick, Sender, Date, Message, Active) VALUES (?, ?, ?, ?, ?, 1)", (message.channel, nick, message.nick, t, msg, ))
        bot.addReply(message.channel, "Message for %s has been recorded and will be delivered once he becomes active again" % nick)
      # Invalid usage
      else:
        bot.addReply(message.channel, "Usage: !tell [nick] [message]")


  def callWatch(self, bot, message):
    if not message.isSystem():
      return

    matchJoin = re.search(self._regexps['join'], message.raw)
    matchNick = re.search(self._regexps['nick'], message.raw)

    if matchJoin:
      nick, channel = matchJoin.groups()
    elif matchNick:
      oldnick, nick = matchNick.groups()
    else:
      return

    exists = bot.database.fetchone("SELECT Nick FROM Mail_messages WHERE Nick = ? AND Active=1 LIMIT 1", (nick, ))
    
    if exists:
        data = bot.database.execute("SELECT Channel, Nick, Sender, Date, Message FROM Mail_messages WHERE Nick = ? AND Active=1",(nick,))

        for row in data:
          bot.addReply(row[0], "%s: Message from %s(posted %s): %s" % (row[1], row[2], row[3], row[4]))

        bot.database.execute("UPDATE Mail_messages SET Active=0 WHERE Nick = ? AND Active=1",(nick,))

