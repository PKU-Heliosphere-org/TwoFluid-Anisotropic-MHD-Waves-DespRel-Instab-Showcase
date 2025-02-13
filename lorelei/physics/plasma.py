r"""
    Plasma.
"""
from numpy import ndarray, sqrt
from numpy.linalg import norm
from typing import List

from lorelei.physics.waves import Wave
from functools import cached_property


class Plasma:
    r"""
        The abstract interface.

        We hope that the values be calculated immediately, so that cached_property is assumed.
    """

    @cached_property
    def f_get_b0(self) -> ndarray:
        ...

    @cached_property
    def b0_norm(self) -> float:
        return norm(self.f_get_b0)

    @cached_property
    def unit_b0(self) -> ndarray:
        return self.f_get_b0 / self.b0_norm

    @cached_property
    def f_get_rho0(self) -> float:
        ...

    @cached_property
    def f_get_p_th0(self) -> float:
        ...

    @cached_property
    def f_get_cs(self) -> float:
        ...

    @cached_property
    def f_get_va(self) -> float:
        return (
            self.b0_norm /
            sqrt(self.f_get_rho0))

    def f_get_wave_modes(self, k: ndarray) -> List[Wave]:
        ...
