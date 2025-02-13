r"""
    One-fluid, isotropic plasma.

    Here we adhere to 8-quantity description (non-conservative).

    They are rho, vx, vy, vz, p_th, Bx, By, Bz.
"""
from typing import List
from lorelei.math.vector import e3, unit
from lorelei.physics.plasma import Plasma
from numpy import ndarray, array as _array, sqrt, abs, dot, zeros
from numpy.linalg import norm
from functools import cached_property

from lorelei.physics.waves import SinusoidalWave, Wave


N_VAR_PLASMA = 8
I_RHO, I_VX, I_VY, I_VZ, I_P_TH, I_BX, I_BY, I_BZ = range(N_VAR_PLASMA)


class AlfvenWave(SinusoidalWave):
    def __init__(
            self, k: ndarray, b0: ndarray, va: float, phase_init: float = 0.0):
        self.k = k
        self.b0 = b0
        self.va = va
        self.e_b0 = unit(b0)
        self.e3 = e3(self.b0, self.k)
        self.phase_init = phase_init

    @cached_property
    def get_omega(self) -> ndarray:
        return self.va * abs(dot(self.k, self.e_b0))

    @cached_property
    def is_acute(self) -> bool:
        return dot(self.b0, self.k) > 0

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        res = zeros(N_VAR_PLASMA)
        b0_norm = norm(self.b0)
        b_v_ratio = b0_norm / self.va
        res[I_VX:I_VZ] = self.e3
        res[I_BX:I_BZ] = (-1.0 if self.is_acute else 1.0) * b_v_ratio * self.e3
        return res

    @cached_property
    def get_phase_init(self) -> float:
        return self.phase_init

    @cached_property
    def get_k(self) -> ndarray:
        return self.k


class IsotropicPlasma(Plasma):
    def __init__(
            self,
            rho0: float = 1.0,
            b0: ndarray = _array((0.0, 0.0, 1.0)),
            p_th0: float = 1.0,
            gamma_gas: float = 5.0 / 3):
        self.rho0 = rho0
        self.b0 = b0
        self.p_th0 = p_th0
        self.gamma_gas = gamma_gas

    @cached_property
    def f_get_b0(self) -> ndarray:
        return self.b0

    @cached_property
    def f_get_rho0(self) -> float:
        return self.rho0

    @cached_property
    def f_get_p_th0(self) -> float:
        return self.p_th0

    @cached_property
    def f_get_cs(self) -> float:
        return sqrt(self.gamma_gas * self.p_th0 / self.rho0)

    def f_get_wave_modes(self, k) -> List[Wave]:
        ...
