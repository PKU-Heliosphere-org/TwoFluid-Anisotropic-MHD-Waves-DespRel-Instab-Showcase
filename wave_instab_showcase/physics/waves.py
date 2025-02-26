r"""
    Waves.
"""


from functools import cached_property
from numpy import ndarray, cos, dot


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


class PlanarWave(SinusoidalWave):
    @cached_property
    def get_k(self) -> ndarray:
        ...

    def phase(self, x: ndarray, t: ndarray) -> ndarray:
        return dot(self.get_k, x) - self.get_omega * t
