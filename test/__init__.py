import sys, untwisted
from testify import *
from twisted.internet import reactor
from twisted.python import log
from untwisted import db, promise, tcp

conn = db.connect(db='cookie', user='root')

listen = tcp.listen(1894)

connect = tcp.connect('localhost', 1438)

def sdfg(cbl):
  log.startLogging(sys.stdout)

  for cursor in conn:
    cursor.execute('DELETE FROM address').execute('DELETE FROM message_id')

  promise.join(*cbl()).then(lambda *_: reactor.stop())

  @untwisted.call
  @promise.continuate
  def _():
    while True:
      ok(False, (yield listen()))

  reactor.callLater(2, reactor.stop)
  reactor.run()

def timeout(secs, *args, **kwds):
  ctx = promise.promise()

  reactor.callLater(secs, untwisted.partial(ctx, *args or (None,), **kwds))

  return ctx
