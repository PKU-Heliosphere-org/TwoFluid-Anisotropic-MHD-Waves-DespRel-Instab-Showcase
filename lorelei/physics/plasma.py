r"""
    Plasma.
"""
from numpy import ndarray, sqrt
from numpy.linalg import norm
from typing import List

from lorelei.physics.waves import Wave


class Plasma:
    def f_get_b0(self) -> ndarray:
        ...

    def f_get_n_e(self) -> float:
        ...

    def f_get_const_mu0(self) -> float:
        ...

    def b0_norm(self) -> float:
        return norm(self.f_get_b0())

    def unit_b0(self) -> ndarray:
        return self.f_get_b0() / self.b0_norm()

    def f_get_rho0(self) -> float:
        ...

    def f_get_p_th0(self) -> float:
        ...

    def f_get_cs(self) -> float:
        ...

    def f_get_va(self) -> float:
        return (
            self.b0_norm() /
            sqrt(self.f_get_const_mu0() * self.f_get_rho0()))

    def f_get_wave_modes(self, k: ndarray) -> List[Wave]:
        ...
