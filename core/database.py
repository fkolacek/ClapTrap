#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Database(object):

  def __init__(self, filename):
    self._filename = filename
    self._conn = sqlite3.connect(filename)

  def __del__(self):
    if self._conn:
      self._conn.close()

  def execute(self, query, args = ()):
    if not self._conn:
      return None

    curr = self._conn.cursor()

    data = curr.execute(query, args)

    self._conn.commit()

    return data

  def fetchone(self, query, args = ()):
    if not self._conn:
      return None

    curr = self.execute(query, args)

    return curr.fetchone()
