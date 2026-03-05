"""
"  screensaver
"""
from multiprocessing import Queue
import pygame


class ScreenSave:
    """
    screensaver

    :param: dict[str, Queue] :
    """
    def __init__(self,
      queue_ : dict[str,Queue]
    ):
        pygame.init()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self._queue = queue_
        self._looping = True
    def _exit(self, signal_ : bool = False)->None:
        if signal_:
            self._queue['slave'].put({
              'name'   : 'screen_saver',
              'status' : 'ended'
            })
        self._looping = False
    def _pong(self, signal_ : bool = False)->None:
        if signal_:
            self._queue['slave'].put({
              'name'   : 'screen_saver',
              'status' : 'pong'
            })
        self._looping = False
    def loop(self)->None:
        """
        main loop

        """
        self._queue['log'].put('screensave start')
        while self._looping:
            if self._queue['master'].empty() is False:
                packet = self._queue['master'].get()
                if packet['command'] == 'exit':
                    self._exit()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self._exit(True)
        self._queue['log'].put('screensave stop')
        pygame.quit()


def screenSaveSubProcess(
  queue_ : dict[str,Queue]
):
    """
    subprocess starter

    :param: dict[str, Queue] :
    """
    (ScreenSave(queue_)).loop()
