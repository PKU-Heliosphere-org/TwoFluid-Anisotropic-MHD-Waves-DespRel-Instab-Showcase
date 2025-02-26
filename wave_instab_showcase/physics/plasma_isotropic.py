r"""
    One-fluid, isotropic plasma.

    We do not consider such a thing like a non-zero v0.

    Here we adhere to 8-quantity description (non-conservative).
    They are rho, vx, vy, vz, p_th, Bx, By, Bz.
"""
from typing import List
from wave_instab_showcase.math.vector import cos_theta, e3, unit
from wave_instab_showcase.physics.plasma import Plasma
from numpy import ndarray, array as _array, sqrt, abs, dot, zeros, empty
from numpy.linalg import norm
from functools import cached_property

from wave_instab_showcase.physics.waves import PlanarWave, SinusoidalWave, Wave


N_VAR_PLASMA = 8
I_RHO, I_VX, I_VY, I_VZ, I_P_TH, I_BX, I_BY, I_BZ = range(N_VAR_PLASMA)


class EntropicMode(PlanarWave):
    def __init__(self, k: ndarray, cs: float, phase_init: float = 0.0):
        self.k = k
        self.cs = cs
        self.phase_init = phase_init

    @cached_property
    def get_omega(self) -> float:
        return 0.0

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        r"""
            We would want a perpendicular mode from those modes with :math:`\delta p = c_s^2 \delta \rho`.

            However, that is not even correct in dimensions.

            Therefore we make it simpler.
        """
        res = zeros(N_VAR_PLASMA)
        res[I_RHO] = 1.0
        res[I_P_TH] = -self.cs ** 2
        return res

    @cached_property
    def get_phase_init(self) -> float:
        return self.phase_init

    @cached_property
    def get_k(self) -> ndarray:
        return self.k


class AlfvenWave(PlanarWave):
    def __init__(
            self, k: ndarray, b0: ndarray, va: float, phase_init: float = 0.0):
        self.k = k
        self.b0 = b0
        self.va = va
        self.e_b0 = unit(b0)
        self.e3 = e3(self.b0, self.k)
        self.phase_init = phase_init

    @cached_property
    def get_omega(self) -> float:
        return self.va * abs(dot(self.k, self.e_b0))

    @cached_property
    def is_acute(self) -> bool:
        return dot(self.b0, self.k) > 0

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        res = zeros(N_VAR_PLASMA)
        b0_norm = norm(self.b0)
        b_v_ratio = b0_norm / self.va
        res[I_VX:I_VZ+1] = self.e3
        res[I_BX:I_BZ+1] = (-1.0 if self.is_acute else 1.0) * b_v_ratio * self.e3
        return res

    @cached_property
    def get_phase_init(self) -> float:
        return self.phase_init

    @cached_property
    def get_k(self) -> ndarray:
        return self.k


class CompressiveWave(PlanarWave):
    def __init__(
            self,
            k: ndarray,
            b0: ndarray,
            va: float,
            cs: float,
            phase_init: float = 0.0,
            is_slow_mode: bool = True):
        self.k = k
        self.b0 = b0
        self.b0_norm = norm(b0)
        self.va = va
        self.cs = cs
        self.e_b0 = unit(b0)
        self.e3 = e3(self.b0, self.k)
        self.phase_init = phase_init
        self.is_slow_mode = is_slow_mode
        self.ek = unit(k)

    @cached_property
    def cos_theta(self) -> float:
        return cos_theta(self.b0, self.k)

    @cached_property
    def get_omega(self) -> float:
        cs2_plus_va2 = self.cs ** 2 + self.va ** 2
        cs2_prod_va2 = self.cs ** 2 * self.va ** 2
        factor = -1.0 if self.is_slow_mode else 1.0
        return (
                0.5 * (
                    cs2_plus_va2 + factor * (
                        cs2_plus_va2**2 -
                        4 * cs2_prod_va2 * self.cos_theta**2) ** 0.5)
            ) ** 0.5

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        res = empty(N_VAR_PLASMA)
        vp = self.get_omega
        d_rho_factor = 1.0
        frac_part = vp / (vp ** 2 - self.cos_theta ** 2 * self.va ** 2)
        d_v_factor_bracket = (
            vp ** 2 * self.ek - self.va ** 2 * self.cos_theta * self.e_b0)
        d_v_factor_bracket_len = norm(d_v_factor_bracket)
        prefix_coef = 1.0 / (d_v_factor_bracket_len * frac_part)
        unit_delta_v = prefix_coef * frac_part * d_v_factor_bracket
        unit_delta_rho = prefix_coef * d_rho_factor
        unit_delta_p = self.cs ** 2 * unit_delta_rho
        d_b_factor_bracket = self.b0_norm / self.va * (
            self.e_b0 - self.cos_theta * self.ek)
        unit_delta_b = prefix_coef * frac_part * d_b_factor_bracket
        res[I_RHO] = unit_delta_rho
        res[I_VX:I_VZ+1] = unit_delta_v
        res[I_P_TH] = unit_delta_p
        # What to do?
        res[I_BX:I_BZ+1] = unit_delta_b
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

    def f_get_wave_modes(self, k, **kwargs) -> List[Wave]:
        r"""
            However, we do not include the mode where :math:`\nabla \cdot \delta \mathbf B = 0`.

            Therefore we have 7 waves, not 8.

            :param kwargs: To change the default behaviour, set `contain_div_b` as True.
        """
        # TODO Contain div B.
        return [
            EntropicMode(k, self.f_get_cs),
            AlfvenWave(k, self.b0, self.f_get_va),
            AlfvenWave(-k, self.b0, self.f_get_va),
            CompressiveWave(k, self.b0, self.f_get_va, self.f_get_cs, is_slow_mode=True),
            CompressiveWave(-k, self.b0, self.f_get_va, self.f_get_cs, is_slow_mode=True),
            CompressiveWave(k, self.b0, self.f_get_va, self.f_get_cs, is_slow_mode=False),
            CompressiveWave(-k, self.b0, self.f_get_va, self.f_get_cs, is_slow_mode=False),
        ]
