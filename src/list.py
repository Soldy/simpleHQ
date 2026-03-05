"""
" file list helper
"""
import os
import sys
from src.hashdict import dictToHash

def getSelf(string_ : str)->str:
    """
    AI generated ??? WTF ??? 

    :param: str :
    :return: str :
    """
    return  string_

def getInteger(string_ : str)->int:
    """
    safe integer from string 

    :param: str :
    :return: str :
    """
    return  int(
      ''.join(filter(str.isdigit, string_))
    )

def pathString(
  path_:str,
  file_:str
)->str:
    """
    path to string 

    :param: str :
    :param: str :
    :return: str :
    """
    return (
      '"'+
      path_+
      '/'+
      file_+
      '"'
    )



def fileList(
  dir_:str,
  end_:int = sys.maxsize,
  start_:int = 0,
  func_ : callable = getSelf
)->list[str]:
    """
    file list 

    :param: str :
    :param: int :
    :param: int :
    :param: callable :
    :return: list[str] :
    """
    serial : int = 0
    files  : list[str] = os.listdir(dir_)
    out    : list[str] = sorted(
      files,
      key=lambda name: name
    )
    return out[start_:end_]

def listMaker(
  dir_ : list[str]
)->list[dict[str,str|int]]:
    out : list[dict[str,str|int]] = []
    for d in dir_:
        for i in fileList(d):
            ff = i.split('.')
            sp = i.split('(')
            date = '0'
            name = ff[0]
            if len(sp) > 1 :
                dt = sp[1].split(')')
                name = str(sp[0])
                date = str(dt[0])
            ref  = dictToHash({
              'name' : name,
              'date' : _date
            })
            one = {
              'id'      : len(out),
              'path'    : str(d),
              'name'    : name,
              'file'    : str(i),
              'date'    : date,
              'ref'     : ref
            }
            out.append(one)
    return sorted(
      out,
      key=lambda one: one['name']
    )
