from typing import NamedTuple

class Token(NamedTuple):
  token: str;
  line: int;
  tokenStartIndex: int;
  tokenEndIndex: int;
  value: str;
