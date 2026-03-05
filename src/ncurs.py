"""
" ncurses menu manager
"""
import sys
import curses
import time
from multiprocessing import Queue, Process
import src.config as conf
from src.dynfile import DynFile
from src.loghelp import logFormat


_chars_in = []
for i in 'qwertyuiopasdfghjklzxcvbnm1234567890 -+.':
    _chars_in.append(ord(i))

class NcursesClass:
    """
    ncurses screen class

    :param: Queue :
    """
    def __init__(
        self,
        queue_ : dict[str, Queue]
    ):
        self._scr = curses.initscr()
        self._log_history : list[str] = []
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self._height : int = 50
        self._width : int = 50
        self._scr.keypad(True)
        self._scr.nodelay(True)
        self._queue : dict[str, Queue] = queue_
        self._list = DynFile(0)
        self._text_filter : str = ''
        self._search_mode : bool = False
        self.updateSize()
        self.loop()
    def updateSize(self)->bool:
        """
        screen size update

        :return: bool :
        """
        height, width = self._scr.getmaxyx()
        if self._height == height and self._width == width:
            return False
        self._height = int(height)
        self._width = int(width)
        self._list.size(self._height-18)
        return True
    def log(self, text_:str)->None:
        """
        log text to screen

        :return: str :
        """
        self._log_history.insert(0,
          logFormat(text_)
        )
        self._renderLog()
    def _renderLog(self)->None:
        self._scr.attron(curses.color_pair(1))
        for h in list(range(len(
          self._log_history[:10]
        ),0, -1)):
            try:
                self._scr.addstr(
                  (10-h),
                  2,
                  (self._log_history[h-1].ljust(self._width-6))[0:(self._width-6)]
                )
            except Exception:
                break
        self._scr.refresh()

    def _renderFilter(self)->None:
        self._scr.addstr(
          (12),
          2,
          self._text_filter.rjust(10, ' ')
        )

    def _renderList(self)->None:
        lista = self._list.get()
        self._scr.attron(curses.color_pair(4))
        for l in range(len(lista)):
            if lista[l][1]:
                self._scr.attron(curses.color_pair(2))
            else:
                self._scr.attron(curses.color_pair(4))
            try:
                self._scr.addstr(
                  (14+l),
                  2,
                  (lista[l][0].ljust(self._width-2))
                )
            except Exception:
                break
        self._scr.refresh()
    def update(self)->None:
        """
        full screen update

        """
        self._list.update()
        if self.updateSize():
            self._renderList()
            self._renderLog()
    def end(self)->None:
        """
        gracefull shutdown

        """
        self._queue['curs'].put({
          'command' : 'exit'
        })
        curses.nocbreak()
        self._scr.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit()
    def _menuSelect(self):
        self._queue['curs'].put({
          'command' : 'play',
          'id'      : int(self._list.active())
        })
    def loop(self):
        """
        main loop 

        """
        looping = True
        check_turn = 0
        while looping:
            check_turn += 1
            time.sleep(conf.tick_delay)
            if self._queue['log'].empty() is False:
                self.log(
                  self._queue['log'].get()
                )
            char : int = self._scr.getch()
            if self._search_mode is True:
                if char in _chars_in:
                    self._text_filter += chr(char)
                    self._list.search(
                      self._text_filter
                    )
                    self._renderFilter()

            elif char == ord('e'):
                self.end()
            elif char == ord('u'):
                self.update()
            elif char == ord('s'):
                self._search_mode = True
            elif char == ord('\n'):
                self._menuSelect()
            elif char == ord('m'):
                self._queue['curs'].put({
                  'command' : 'menu',
                  'id'      : int(self._list.active())
                })
            if char == curses.KEY_BACKSPACE:
                if len(self._text_filter) > 0:
                    self._text_filter = self._text_filter[:-1]
                    self._renderFilter()
            if char == curses.KEY_HOME:
                if self._search_mode is True:
                    self._search_mode = False
            elif char == curses.KEY_UP:
                self._list.up()
            elif char == curses.KEY_DOWN:
                self._list.down()
            elif char == curses.KEY_ENTER:
                self._menuSelect()
            self._renderList()
            if check_turn >= 20:
                check_turn = 0
                self.update()


def cursesStart(
  queue_ : dict[str, Queue]
):
    """
    sub process holder function


    :param: Queue :
    """
    (NcursesClass(queue_))

def startCurses(
  queue_ : dict[str, Queue]
):
    """
    sub process start


    :param: Queue :
    """
    proc = Process(
      target=cursesStart,
      args=(
        queue_,
      )
    )
    proc.start()
