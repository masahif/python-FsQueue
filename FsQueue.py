""" FsQueue
   Elastic queue is based on filesystem.
   It's like almost same as Python's Queue.Queue.
"""

__author__ = 'FUKUDA Masahiro'
__author_email__ = 'masahiro@fukuda.org'
__version__ = '1.2'
__all__ = ['Empty', 'Full', 'Queue']

import tempfile, os
import pickle
from time import sleep
import Queue
import time

try:
    import threading
except ImportError:
    import dummy_threading as threading

Empty = Queue.Empty
Full  = Queue.Full

_count_mutex = threading.Lock()
_count = 0

def _counter():
    global _count_mutex, _count
    try:
        _count_mutex.acquire()
        return _count
    finally:
        _count += 1
        _count_mutex.release()

class Queue(object):
    """Create a queue object.
    """

    def __init__(self, maxsize=0, dir='_tmp_fsqueue', init=False):
        self.base_dir = dir
        self.queue_dir = os.path.join(dir, 'queue')
        self.tmp_dir = os.path.join(dir, 'tmp')
        self.count_dir = os.path.join(dir, 'count')

        if init:
            self.init_queue()

        try:
            os.mkdir(dir, 0700)
        except OSError:
            pass

        try:
            os.mkdir(self.queue_dir, 0700)
        except OSError:
            pass

        try:
            os.mkdir(self.tmp_dir, 0700)
        except OSError:
            pass

        try:
            os.mkdir(self.count_dir, 0700)
        except OSError:
            pass

    def task_done(self):
        for f in os.listdir(self.count_dir):
            try:
                os.rmdir(os.path.join(self.count_dir, f))
                return
            except OSError:
                pass
            
        raise ValueError('task_done() called too many times')

    def join(self):
        while(not self.empty()):
            #print "wait queue become empty."
            sleep(0.1)

    def qsize(self):
        return len(os.listdir(self.queue_dir))

    def empty(self):
        return self.qsize() == 0

    def full(self):
        # full() is not supported.
        # always return "False"
        return False

    def put(self, item, block=True, timeout=None):
        tmpf = tempfile.mkstemp('', '', self.tmp_dir)
        tmpfd = os.fdopen(tmpf[0], "w")
        pickle.dump(item, tmpfd, pickle.HIGHEST_PROTOCOL)
        tmpfd.close()
        basename = os.path.basename(tmpf[1])
        os.rename(tmpf[1],
                   os.path.join(self.queue_dir,
                                "%s.%s.%s" % (os.stat(tmpf[1]).st_mtime, _counter(), basename)))

        os.mkdir(os.path.join(self.count_dir, basename), 0700)

    def put_nowait(self, item):
        return self.put(item, False)

    def get_nowait(self):
        try:
            queues = os.listdir(self.queue_dir)
        except OSError:
            raise Empty
        
        queues.sort()

        tmp = None

        for q in queues:
            src = os.path.join(self.queue_dir, q)
            dst = os.path.join(self.tmp_dir, q)
            try:
                os.rename(src, dst)
                tmp = dst
                break
            except OSError:
                continue

        if tmp is None:
            raise Empty

        f = open(tmp, 'r')
        data = pickle.load(f)
        f.close()
        os.unlink(tmp)

        return data

    def get(self, block=True, timeout=None):
        endtime = time.time() + timeout if timeout else None
        
        while(True):
            try:
                return self.get_nowait()
            except Empty:
                time.sleep(0.01)
                if endtime and endtime - time.time() <= 0.0:
                    raise Empty

    def init_queue(self):
        import shutil
        shutil.rmtree(self.base_dir)


if __name__ == "__main__":
    q = Queue()

    for a in xrange(10):
        q.put('ikatako' * a)
    
    while(True):
        try:
            print q.get_nowait()
        except Empty:
            break

    print "wait"
    q.join()
    print "end"
