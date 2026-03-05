"""
" video player agent
"""
import subprocess
from multiprocessing import Queue
from src.list import pathString


def videoFilePlay(
  queue_  : dict[str,Queue],
  player_ : str,
  file_   : dict[str,str]
)->None:
    """
    Player loop

    :param: dict[str, Queue] :
    :param: str :
    :param: dict[str, str] :
    """
    errored = False
    play = (
      player_+
      ' '+
      pathString(
        file_['path'],
        file_['file']
      )
    )
    with subprocess.Popen(
      play,
      shell=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT
    ) as p:
        line = ''
        serial = 0
        queue_['log'].put('play start : '+file_['ref'])
        while True:
            char = p.stdout.read(1)
            if p.poll() is not None:
                break
            if char == b'\r':
                packet = {
                  'name'   : 'player',
                  'status' : 'run',
                  'serial' : str(serial),
                  'line': line
                }
#                queue_['slave'].put(packet)
                line = ''
                serial += 1
                continue
            try:
                line += str(char.decode("utf-8"))
            except Exception:
                if errored is False:
                    queue_['log'].put('play error : '+file_['ref'])
                errored = True
        packet = {
          'name'   : 'player',
          'status' : 'ended',
          'serial' : str(serial),
          'line': ''
        }
        queue_['slave'].put(packet)
        queue_['log'].put('play end : '+file_['ref'])
        p.terminate()
