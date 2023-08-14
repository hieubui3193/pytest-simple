"""
Support module.
"""
from typing import Iterator, Optional
import io


class StringIteratorIO(io.TextIOBase):
    """
    This class support reduce memory used in transfer data process to db.
    """

    def __init__(self, _iter: Iterator[str]):
        self._iter = _iter
        self._buff = ''

    def readable(self) -> bool:
        return True

    def _read1(self, num: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:num]
        self._buff = self._buff[len(ret):]
        return ret

    def read(self, num: Optional[int] = None) -> str:
        line = []
        if num is None or num < 0:
            while True:
                temp = self._read1()
                if not temp:
                    break
                line.append(temp)
        else:
            while num > 0:
                temp = self._read1(num)
                if not temp:
                    break
                num -= len(temp)
                line.append(temp)
        return ''.join(line)
