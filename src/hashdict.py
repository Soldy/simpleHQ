import json
import hashlib


def dictToHash(in_ : dict[str,str])->str:
    return hashlib.sha3_512(
      (json.dumps(in_)).encode()
    ).hexdigest()
