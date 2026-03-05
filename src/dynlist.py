"""
dynamic list Manager
"""
from copy import deepcopy


class DynList:
    """
    DynList Class

    :param: int :
    """
    def __init__(
      self,
      size_ : int,
      list_ : list[dict[str,str|int]] = [],
      active_ : int = 0
    ):
        self._list : list[dict[str,str|int]] = list_
        self._active : int = active_
        self._size : int = int(size_)
    def _listOut(
      self, start_ : int,
      end_ : int
    )->list[tuple[str,bool]]:
        """
        list output formater

        :param: int :
        :param: int :
        :return: list[tuple[str,bool]] :
        """
        out : list[tuple[str,bool]] = []
        for i in list(range(start_, end_)):
            if i == self._active:
                out.append(
                  (
                    str(self._list[i]['name']),
                    True
                  )
                )
            else:
                out.append(
                  (
                    str(self._list[i]['name']),
                    False
                  )
                )
        return out
    def get(self)->list[tuple[str,bool]]:
        """
        get a screen load list

        :return: list[tuple[str,bool]] :
        """
        if self._size > len(self._list):
            return self._listOut(0, len(self._list))
        elif (self._size/2) > self._active:
            return self._listOut(0, self._size)
        elif self._active > (len(self._list) - int(self._size/2)):
            return self._listOut(
              (len(self._list)-self._size),
              len(self._list)
            )
        else:
            half = int(self._size/2)
            return self._listOut(
              (self._active-half),
              (self._active+half)
            )
    def search(
      self,
      text_ : str,
      size_ : int = 1
    )->list[int]:
        """
        search element on the list

        :param: str :
        :param: int :
        :return: listi[int] :
        """
        out : list[int] = []
        serial = 0
        for i in range(len(self._list)):
            if text_.lower() in (self._list[i]['name']).lower():
                out.append(i)
                serial += 1
            if serial >= size_:
                break
        if len(out) > 0:
            self.set(out[0])
        return out
    def update(self, list_ : list[dict[str,str]])->None:
        """
        set the active element

        :param: list[dict[str,str]]:
        """
        self._list = list_
        self._list = deepcopy(list_)
    def set(self, select_ : int)->int:
        """
        set the active element

        :param: int :
        :return: int :
        """
        if 0 > select_:
           self._active = len(self._list)-1
        elif select_ >= len(self._list):
           self._active = 0
        else:
           self._active = int(select_)
        return int(self._active)
    def up(self)->int:
        """
        move up in the list 

        :return: int :
        """
        return self.set(self._active-1)
    def down(self)->int:
        """
        move up in the list 

        :return: int :
        """
        return self.set(self._active+1)
    def active(self)->int:
        """
        active index

        :return: int :
        """
        return int(
          self._active
        )
    def size(self, size_ : int)->None:
        """
        size

        :param: int :
        """
        self._size = size_
