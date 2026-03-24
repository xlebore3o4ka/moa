from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceInfo:
    file: str
    max_addr: int
    line: int
    col: int
    length: int


class SourceMap:
    def __init__(self, source: str):
        self._intervals: list[SourceInfo] = []
        self.source = source

    def add(self, file: str, max_addr: int, line: int, col: int, length: int):
        self._intervals.append(SourceInfo(file, max_addr, line, col, length))

    def get(self, pc: int) -> Optional[SourceInfo]:
        lo, hi = 0, len(self._intervals)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._intervals[mid].max_addr < pc:
                lo = mid + 1
            else:
                hi = mid
        if lo < len(self._intervals):
            return self._intervals[lo]
        return None
