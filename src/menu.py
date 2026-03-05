"""
" pygame menu manager
"""
import copy
import time
from multiprocessing import Queue
import pygame
import src.config as conf
from src.dynlist import DynList

class BigMenuClass:
    """
    pygame screen class

    :param: Queue :
    :param: list[dict[str,str]] :
    :param: int :
    :param: str :
    """
    def __init__(
      self,
      queue_  : dict[str,Queue],
      list_   : list[dict[str,str]],
      active_ : int = 0,
      name_   : str = 'play'
    ):
        pygame.init()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self._name  : str = name_
        self._queue : dict[str, Queue] = queue_
        self._updateable : int = 0
        self._screen : callable = pygame.display.set_mode(
          (1920, 1080)
        )
        self._clock : callable = pygame.time.Clock()
        self._key : int = 0
        self._key_last : int = 0
        self._key_repeat : int = 0
        self._key_unicode : str = ''
        self._looping : bool = True
        self._list = DynList(20, list_, active_)
        self._font = pygame.font.SysFont(None, 48)
        self._text_filter : str = ''
        self._search_mode : bool = False
        self.text = ''
    def _menuColor(self, active_: bool = False)->list[int]:
        if active_ :
            return [140, 140, 140]
        return [100, 100, 100]

    def _renderFilter(self)->None:
        self._screen.blit(
            self._font.render(
                f'{self._text_filter}',
                True,
                self._menuColor()
            ),
            (100, (40))
        )

    def _renderList(self)->None:
        lista = self._list.get()
        for i in range(len(lista)):
            mp = lista[i]
            self._screen.blit(
                self._font.render(
                    f'{mp[0]}',
                    True,
                    self._menuColor(
                      mp[1]
                    )
                ),
                (100, (i*40)+240)
            )
    def _change(self, status_ : str =  'change'):
        self._queue['slave'].put({
          'name'    : str(self._name),
          'status'  : status_,
          'id'      : int(self._list.active())
        })
    def _menuSelect(self):
        self._change('ended')
        self._looping = False
    def _keyPressed(self):
        ctime : int = int(time.time()*1000)
        self._updateable = 0
        if self._key == 0:
            return
        if (
          self._key_repeat < conf.sdl_key_repeat_slow and
          self._key_last + conf.sdl_key_repeat > ctime
        ):
            return
        if (
          self._key_last + conf.sdl_key_repeat_after > ctime
        ):
            return
        self._key_repeat += 1
        self._key_last = int(time.time()*1000)
        if self._key == 1073741905:
            self._list.down()
        elif self._key == 1073741906:
            self._list.up()
        elif self._key == pygame.K_RETURN:
            self._menuSelect()
            return
        elif self._key == pygame.K_BACKSPACE:
            if len(self._text_filter) > 0:
                self._text_filter = self._text_filter[:-1]
                self._renderFilter()
                self._list.search(
                  self._text_filter
                )
        else:
            self._text_filter += self._key_unicode
            self._list.search(
              self._text_filter
            )
        self._change()
    def _keyProcess(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._key_repeat = 0
                self._key = copy.deepcopy(event.key)
                self._key_unicode = copy.deepcopy(
                  event.unicode
                )
            if event.type == pygame.KEYUP:
                self._key = 0
        self._keyPressed()
    def loop(self):
        """
        main loop

        """
        self._queue['log'].put('menu start')
        self._looping = True
        while self._looping:
            self._keyProcess()
            if self._queue['master'].empty() is False:
                packet = self._queue['master'].get()
                if packet['command'] == 'exit':
                    self._queue['log'].put('menu stop signal')
                    self._looping = False
            if self._updateable < 5:
                self._screen.fill([0,0,0])
                self._renderList()
                self._renderFilter()
                pygame.display.flip()
                self._updateable += 1
            else:
                pygame.time.wait(15)
        self._queue['log'].put('menu stop')
        pygame.quit()


def menuSubProcess(
  queue_  : dict[str,Queue],
  lista_  : list[dict[str,str]],
  active_ : int = 0
):
    """
    sub process holder function


    :param: dict[str, Queue] :
    :param: list[dict[str, str]] :
    :param: int :
    """
    (BigMenuClass(
      queue_,
      lista_,
      active_
    )).loop()
