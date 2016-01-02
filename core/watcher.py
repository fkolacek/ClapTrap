#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Based on LogWatcher from: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
# Source: http://code.activestate.com/recipes/577968-log-watcher-tail-f-log/
# License: MIT

import os
import time
import stat
import sys
import errno
import fnmatch

class Watcher:
  def __init__(self, folder, callback, patterns=['*.log'], sizehint=1040576):
    self.folder = os.path.realpath(folder)
    self.patterns = patterns

    self._filesMap = {}
    self._callback = callback
    self._sizehint = sizehint

    assert os.path.isdir(self.folder), self.folder
    assert callable(callback), repr(callback)

    self.updateFiles()

    for id, file in self._filesMap.items():
      file.seek(os.path.getsize(file.name))

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.close()

  def __del__(self):
    self.close()

  def loop(self, interval=0.1, blocking=True):
    while True:
      self.updateFiles()

      for fid, file in list(self._filesMap.items()):
        self.readlines(file)

      if not blocking:
        return

      time.sleep(interval)

  def log(self, line):
    print line

  def listdir(self):
    files = []

    for root, dirnames, filenames in os.walk(self.folder):
      for pattern in self.patterns:
        for filename in fnmatch.filter(filenames, pattern):
          files.append(os.path.join(root, filename))

    return list(set(files))

  @classmethod
  def open(cls, file):
    return open(file, 'rb')

  @classmethod
  def tail(cls, fname, window):
    if window <= 0:
      raise ValueError('Invalid window value')

    with cls.open(fname) as f:
      BUFSIZ = 1024

      encoded = getattr(f, 'encoding', False)
      CR = '\n' if encoded else b'\n'
      data = '' if encoded else b''

      f.seek(0, os.SEEK_END)
      fsize = f.tell()
      block = -1
      exit = False

      while not exit:
        step = (block * BUFSIZ)
        if abs(step) >= fsize:
          f.seek(0)
          newdata = f.read(BUFSIZ)
        data = newdata + data
        if data.count(CR) >= window:
          break
        else:
          block -= 1
      return data.splitlines()[-window:]

  def updateFiles(self):
    ls = []
    for name in self.listdir():
      absname = os.path.realpath(os.path.join(self.folder, name))
      try:
        st = os.stat(absname)
      except EnvironmentError as err:
        if err.errno != errno.ENOENT:
          raise
      else:
        if not stat.S_ISREG(st.st_mode):
          continue
        fid = self.getFileId(st)
        ls.append((fid, absname))

    # Check the existing ones
    for fid, file in list(self._filesMap.items()):
      try:
        st = os.stat(file.name)
      except EnvironmentError as err:
        if err.errno == errno.ENOENT:
          self.unwatch(file, fid)
        else:
          raise
      else:
        if fid != self.getFileId(st):
          self.unwatch(file, fid)
          self.watch(file.name)

    # Check new ones
    for fid, fname in ls:
      if fid not in self._filesMap:
        self.watch(fname)

  def readlines(self, file):
    while True:
      lines = file.readlines(self._sizehint)
      if not lines:
        break
      self._callback(file.name, lines)

  def watch(self, fname):
    try:
      file = self.open(fname)
      fid = self.getFileId(os.stat(fname))
    except EnvironmentError as err:
      if err.errno != errno.ENOENT:
        raise
    else:
      self.log("[*] Watching file %s" % fname)
      self._filesMap[fid] = file

  def unwatch(self, file, fid):
    self.log("[*] Un-watching file %s" % file.name)
    del self._filesMap[fid]
    while file:
      lines = self.readlines(file)
      if lines:
        self._callback(file.name, lines)

  @staticmethod
  def getFileId(st):
    if os.name == 'posix':
      return "%xg%x" % (st.st_dev, st.st_ino)
    else:
      return "%f" % st.st_ctime

  def close(self):
    for id, file in self._filesMap.items():
      file.close()
    self._filesMap.clear()

