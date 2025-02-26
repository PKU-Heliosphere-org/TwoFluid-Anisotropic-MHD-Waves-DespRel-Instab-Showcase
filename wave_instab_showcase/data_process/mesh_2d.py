r"""
    2D Data Generator.
"""


from dataclasses import dataclass
from functools import cached_property
from typing import Callable, Tuple
from numpy import ndarray, empty, arange, meshgrid


@dataclass
class Cadence:
    x_start: float
    n: float
    dx: float

    def x(self, i: float) -> float:
        return self.x_start + i * self.dx

    def i(self, x: float) -> float:
        return (x - self.x_start) / self.dx

    @cached_property
    def stencil(self) -> ndarray:
        return self.x_start + arange(self.n) * self.dx


@dataclass
class Mesh:
    x: Cadence
    y: Cadence

    def get_scalar(self, source: Callable[[float, float], float]) -> ndarray:
        res = empty((self.x.n, self.y.n))
        for i in range(self.x.n):
            x = self.x.x(i)
            for j in range(self.y.n):
                y = self.y.x(j)
                res[i, j] = source(x, y)
        return res

    def get_vector_field_slice(
            self,
            source: Callable[[float, float], ndarray],
            is_vec_2d: bool = False) -> ndarray:
        res = empty((self.x.n, self.y.n, 2 if is_vec_2d else 3))
        for i in range(self.x.n):
            x = self.x.x(i)
            for j in range(self.y.n):
                y = self.y.x(j)
                res[i, j, :] = source(x, y)
        return res

    @cached_property
    def mesh_x_y(self) -> Tuple[ndarray, ndarray]:
        x_pt = self.x.stencil
        y_pt = self.y.stencil
        x_grid, y_grid = meshgrid(x_pt, y_pt)
        return x_grid, y_grid
