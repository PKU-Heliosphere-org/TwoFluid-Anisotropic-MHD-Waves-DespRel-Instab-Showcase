r"""
    Waves.
"""


from functools import cached_property
from typing import Callable, Iterable
from numpy import empty, ndarray, cos, dot, array as _array


class Wave:
    r"""
        Wave features.
    """
    @cached_property
    def get_omega(self) -> float | complex:
        ...

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        ...

    def unit_osc_at(self, x: ndarray, t: ndarray) -> ndarray:
        r"""
            We do not assume a priori that the wave be planar or even
            sinusoidal.

            Thence, the interface is left virtual for the sake of specified
            waves.
        """
        ...


class SinusoidalWave(Wave):
    def __init__(self):
        super().init()

    @cached_property
    def get_phase_init(self) -> float:
        ...

    def phase(self, x: ndarray, t: ndarray) -> ndarray:
        r"""
            Note: we should include phase_init in this result.
        """
        ...

    def unit_osc_at(self, x: ndarray, t: ndarray) -> ndarray:
        return self.get_unit_energy_oscillation * cos(self.phase(x, t))

    def make_scalar_taker_zox_at_t_0(self, i_quan: int) -> Callable[[float, float], float]:
        f = self.unit_osc_at

        def taker(z: float, x: float) -> float:
            res = f(_array((x, 0.0, z)), 0.0)
            return res[i_quan]
        return taker

    def make_vector_taker_zox_at_t_0(self, i_quan: Iterable[int]) -> Callable[[float, float], ndarray]:
        f = self.unit_osc_at

        def taker(z: float, x: float) -> ndarray:
            info = f(_array((x, 0.0, z)), 0.0)
            res = empty(len(i_quan))
            for i, i_info in enumerate(i_quan):
                res[i] = info[i_info]
            return res
        return taker


class PlanarWave(SinusoidalWave):
    def __init__(self):
        super().init()

    @cached_property
    def get_k(self) -> ndarray:
        ...

    def phase(self, x: ndarray, t: ndarray) -> ndarray:
        return dot(self.get_k, x) - self.get_omega * t
