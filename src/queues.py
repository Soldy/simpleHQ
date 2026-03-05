"""
Queue Manager
"""
from multiprocessing import Queue

class QueueManager:
    """
    Queue Manager
    """
    def __init__(self):
        self.log    : Queue = Queue()
        self.curs   : Queue = Queue()
        self.slave  : Queue = Queue()
        self.master : Queue = Queue()

    def update(self):
        """
        Queue master replacer
        """
        self.master = Queue()
    def hq(self):
        """
        Queue for main hq
        """
        return {
          'slave'  : self.slave,
          'curs'   : self.curs,
          'log'    : self.log
        }

    def curses(self):
        """
        Queue for curse menu
        """
        return {
          'slave'  : self.slave,
          'curs'   : self.curs,
          'log'    : self.log
        }

    def slaves(self):
        """
        Queue for a slave
        """
        return {
          'slave'  : self.slave,
          'master' : self.master,
          'log'    : self.log
        }
