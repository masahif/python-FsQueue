==========
FsQueue
==========

python FsQueue is a elastic synchronized queue class.


Features
===========
The FsQueue module has almost same as python's queue class.

- FsQueue is elastic.
- FsQueue is multi process safe. Multi process can work with FsQueue.
- FsQueue doesn't have max size feature so full() always return False.
- FsQueue might work as FIFO queue.


A quick example
===================

example::
  
  import sys
  from multiprocessing import Process
  from DiskQueue import Queue
  from time import sleep
  
  MAX_TRY = 1000
  
  def put(q):
      for i in xrange(MAX_TRY):
          print "put:%d" % i
          sys.stdout.flush()
          q.put('hoge')
  
  def get(q):
      for i in xrange(MAX_TRY):
          print "get:%d" % i
          sys.stdout.flush()
          q.get()
          q.task_done()
  
  def process_test():
      q = Queue()
      p0 = Process(target=put, args=(q,))
      p1 = Process(target=get, args=(q,))
      p1.start()
      p0.start()
      p0.join()
      p1.join()


Recent Change Log
======================

v1.0
-------
 * First release
