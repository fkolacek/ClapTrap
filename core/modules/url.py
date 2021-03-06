#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2
from BeautifulSoup import BeautifulSoup

class Url(object):

  meta = {
    'name': "Url",
    'description': "",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "0.1",
    'triggers': {
      '(https?:\/\/([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.\-=\?\~_;+%#&:]*)\/?)': "grabUrl"
    }
  }

  def __init__(self, bot):
    pass

  def grabUrl(self, bot, message):
    for trigger, callback in self.meta['triggers'].iteritems():
      if callback == "callGrabUrl":
        break

    match = re.search(trigger, message.message)

    if match:
      url = match.group(1)

      print "[*] Grab URL: %s" % url

      soup = BeautifulSoup(urllib2.urlopen(url),convertEntities=BeautifulSoup.HTML_ENTITIES)
      title = soup.title.string.encode('utf-8', 'ignore')

      if title.count('\n') > 8:
        bot.addReply(message.channel, "%s: %s" % (message.nick, "it's not funny anymore!"))

      bot.addReply(message.channel, "[%s]" % title.split('\n', 1)[0].strip())


