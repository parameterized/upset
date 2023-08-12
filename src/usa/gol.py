import random

import numpy as np

from pyodide.ffi import to_js
from js import Uint8ClampedArray

from usa.usa import USA


GOL_ELEMENT = tuple[int, int, int]


class GOL(USA):
    S_i: set[GOL_ELEMENT]
    size: int

    def __init__(self, size: int) -> None:
        super().__init__()
        self.size = size
        for i in range(size):
            for j in range(size):
                self.S_i.add((i, j, random.choice([0, 1])))

    def neighbors(self, element: GOL_ELEMENT) -> int:
        x, y, _ = element
        return sum(
            ((x + dx) % self.size, (y + dy) % self.size, 1) in self.S_i
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx, dy) != (0, 0)
        )

    def delta(self, element: GOL_ELEMENT) -> tuple[set, set]:
        x, y, a = element
        n = self.neighbors(element)
        if a == 1 and n not in {2, 3}:
            return ({(x, y, 0)}, {element})
        elif a == 0 and n == 3:
            return ({(x, y, 1)}, {element})

        return (set(), set())


def upsample(
    image: np.ndarray,
    res: int,
) -> np.ndarray:
    """
    Nearest neighbor upsample a (N, N, C) image to the specified resolution.
    res should be a multiple of N.
    """
    h, w = image.shape[:2]
    return image.repeat(res // h, axis=0).repeat(res // w, axis=1)


class CellRenderer:
    def __init__(self, cell_usa: USA):
        self.cell_usa = cell_usa

    def render(self) -> Uint8ClampedArray:
        rgba_list = []
        size = self.cell_usa.size
        for i in range(size):
            for j in range(size):
                alive = (i, j, 1) in self.cell_usa.S_i
                r, g, b = (0, 0, 0) if alive else (255, 255, 255)
                rgba_list.append([r, g, b, 255])

        img = np.array(rgba_list, dtype=np.uint8).reshape(size, size, 4)
        img_ups = upsample(img, size * 10)
        return Uint8ClampedArray.new(to_js(img_ups.reshape(-1)))
