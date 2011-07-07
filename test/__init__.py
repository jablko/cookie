import MySQLdb, sys, untwisted
from testify import *
from twisted.internet import reactor
from twisted.python import log
from untwisted import promise, tcp

conn = MySQLdb.connect(db='cookie', user='root')

listen = tcp.listen(1894)

connect = tcp.connect('localhost', 1438)

def sdfg(cbl):
  log.startLogging(sys.stdout)

  cursor = conn.cursor()
  cursor.execute('DELETE FROM address')
  cursor.execute('DELETE FROM message_id')
  cursor.close()

  cbl()

  @untwisted.call
  @promise.continuate
  def _():
    while True:
      ok(False, (yield listen()))

  reactor.callLater(2, reactor.stop)
  reactor.run()
