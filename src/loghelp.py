import datetime

def logFormat(
  text_ : str,
  max_: int = 500
)->str:
    return (
      " "+
      datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
      )+
      " : "+
      text_
    )[0:max_]
