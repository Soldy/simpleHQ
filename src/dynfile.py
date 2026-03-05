"""
" dyn file class
"""
import src.config as conf
from src.dynlist import DynList
from src.list import listMaker


class DynFile(DynList):
    """
    DynList Class

    :param: int :
    """
    def __init__(
      self,
      size_ : int,
      list_ : list[dict[str,str]] = listMaker(conf.dirs),
      active_ : int = 0
    ):
        super().__init__(
          size_,
          list_,
          active_
        )
    def update(
      self,
    )->None:
        """
        set the active element
 
        :param: list[dict[str,str]]:
        """
        super().update(listMaker(conf.dirs))
