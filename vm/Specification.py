from typing import Literal


class Specification:
    def __init__(self,
                 bitness: Literal[8, 16, 32, 64] = 32,
                 byteorder: Literal["little", "big"] = "little",
                 colored_error: bool = False):
        self.BITNESS: Literal[8, 16, 32, 64]     = bitness
        self.BYTEORDER: Literal["little", "big"] = byteorder
        # always unsigned

        _bitness_map = {8: ("B", 1), 16: ("H", 2), 32: ("I", 4), 64: ("Q", 8)}
        if self.BITNESS not in _bitness_map: raise ValueError(f"Unsupported bitness: {self.BITNESS}")
        self.BITNESS_MASK = 2 ** self.BITNESS - 1
        self.TYPECODE, self.BYTELENGTH = _bitness_map[self.BITNESS]
        self.BYTELENGTH_SHIFT = self.BYTELENGTH.bit_length() - 1
        self.pack = lambda value: value.to_bytes(self.BYTELENGTH, self.BYTEORDER, signed=False)

        self.COLORED_ERROR: bool = colored_error
