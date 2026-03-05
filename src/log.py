import time
import src.config as conf
from src.loghelp import logFormat
from multiprocessing import Queue, Process

__queue : Queue = Queue()

def logPut()->callable:
    return __queue

class LogClass:
    def __init__(
      self,
      func_  : callable
    ):
        self._print = func_
        self._queue = logPut()
        self.loop()
    def log(self, text_ : str)->None:
        self._print(logFormat(text_))
    def loop(self)->None:
        while True:
            time.sleep(0.05)
            if self._queue.empty() == False:
                self.log(
                  self._queue.get()
                )

def log(
  func_  : callable
):
    (LogClass(func_))

def startLog(
  func_  : callable = print
):
    proc = Process(
      target=log,
      args=(
        func_,
      )
    )
    proc.start()


startLog()
