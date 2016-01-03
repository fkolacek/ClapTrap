#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Controller(object):

  def __init__(self, bot):
    self._nick = bot.config['nick']
    self._channels = bot.config['channels']

    self._regexps = {
        # /home/bb8/ClapTrap/ircdir/irc.freenode.org/#fitgame/out: 2016-01-03 03:30 -!- Brano kicked Clap_Trap ("Autoreconnect?")
        # /home/bb8/ClapTrap/ircdir/irc.freenode.org/#fitgame/out: 2016-01-03 09:53 -!- Clap_Trap(~Clap_Trap@saber.sniff.ws) has joined #fitgame
        # 
      'part': '',
      'join': '',
      'kick': '',
    }

  def processMessage(self, bot, message):
    if message.isSystem():
      
      pass
    elif message.isValid():

      pass
    else:
      pass
