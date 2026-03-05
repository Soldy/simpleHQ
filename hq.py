"""
" Hq main
"""
import time
import sys
from multiprocessing import Process
import src.config as conf
from src.queues import QueueManager
from src.list import listMaker
from src.play import videoFilePlay
from src.menu import menuSubProcess
from src.ncurs import startCurses, NcursesClass
from src.screensave import screenSaveSubProcess


def sleep():
    """
    temp unified sleep function

    """
    time.sleep(conf.change_delay)


class MainClass:
    """
    main adent class

    """
    def __init__(
      self,
    ):
        self._active : int = 0
        self._queue  : QueueManager = QueueManager()
        self._curs   : NcursesClass  = startCurses(
           self._queue.curses()
        )
        self._video_list  = listMaker(conf.dirs)
        self._status      = 'nothing'
        self._status_last = 'nothing'
        self._start_time  = int(time.time())
        self._screen : Process
        self._videoMenu()
        self.loop()

    def _statusChange(self, status_ :str)->None:
        self._status_last = str(self._status)
        self._status      = str(status_)

    def _screenClean(self):
        try:
            sleep()
            self._screen.kill()
        except Exception:
            self._queue.log.put('screen clean error')
            return

    def _screenQueueUpdate(self)->None:
        self._screenClean()
        self._queue.update()

    def _screenProcess(
      self,
      name_ : str,
      func_ : callable,
      args_ : tuple = tuple()
    ):
        self._screenQueueUpdate()
        self._screen = Process(
          target=func_,
          args=(
            (self._queue.slaves(),)+args_
          )
        )
        self._screen.start()
        self._statusChange(name_)

    def _play(self):
        self._screenProcess(
          'play',
          videoFilePlay,
          (
            conf.video_player,
            self._video_list[self._active]
          )
        )

    def _videoMenu(self)->None:
        self._screenProcess(
          'menu_play',
          menuSubProcess,
          (
            self._video_list,
            self._active
          )
        )
        self._start_time  = int(time.time())

    def _screenSaver(self)->None:
        self._screenProcess(
         'screensaver',
          screenSaveSubProcess
        )

    def _screenSaverTimeCheck(self)->bool:
        if (self._status in  ['screensaver','play']):
            return False
        if (
          (self._start_time+conf.screen_delay) > int(time.time())
        ):
            return False
        self._queue.master.put({
          'command':'exit'
        })
        self._screenSaver()
        return True

    def _decession(self, packet : dict[str, str|int])->str:
        if self._status == 'menu_play':
            self._active = int(packet['id'])
            self._play()
        elif self._status == 'screensaver':
            self._videoMenu()
        elif self._status == 'play':
            self._videoMenu()

    def _changeActive(
      self,
      packet : dict[str, str|int]
    )->None:
        self._active = int(packet['id'])

    def loop(self)->None:
        """
        loop runner


        """
        looping = True
        while looping:
            if self._queue.slave.empty() is False:
                packet = self._queue.slave.get()
                self._start_time = int(time.time())
                if packet['status'] == 'ended':
                    self._decession(packet)
                if packet['status'] == 'change':
                    self._changeActive(packet)
            if self._queue.curs.empty() is False:
                packet = self._queue.curs.get()
                if packet['command'] == 'play':
                    self._changeActive(packet)
                    self._play()
                if packet['command'] == 'menu':
                    self._screen.kill()
                    sleep()
                    self._start_time = int(time.time())
                    self._videoMenu()
                elif packet['command'] == 'exit':
                    self._queue.log.put('exit')
                    self._screenClean()
                    sys.exit()
            else:
                self._screenSaverTimeCheck()
            time.sleep(conf.tick_delay)


if __name__ == '__main__':
    (MainClass())
