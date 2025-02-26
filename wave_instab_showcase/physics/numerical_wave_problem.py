r"""
    Wave problem in general.

    If we model using the wave problem, it means we want to have a numerical
    solution of the following equation

    .. math::

        \mathbf W_{, t} + \mathsf A \cdot \mathbf W_{, x} = \mathbf 0

    Currently we ignore the source terms.
    Here we pre-assume :math:`\hat{\mathbf x}` along :math:`\mathbf k`.

    It is easy to verify that if :math:`\mathfrak r` is the right eigenvector
    of :math:`\mathsf A` with the corresponding eigenvalue :math:`\lambda`,
    the wave :math:`\exp{\mathrm i \cdot(k x - \omega t)} \mathfrak r`
    is a solution to the wave equation.

    Hence, we have
    1.  The eigenvalue is the phase velocity.
    2.  The eigenvector is the polarization.
"""

from dataclasses import dataclass
from functools import cached_property
from numpy import ndarray
from numpy.linalg import eig
from typing import List

from wave_instab_showcase.physics.waves import PlanarWave


class NumericalPlanarWaveOrInstab(PlanarWave):
    def __init__(
            self,
            k: ndarray,
            omega: float | complex,
            polarization: ndarray,
            phase_init: float = 0.0):
        self.k = k
        self.omega = omega
        self.polarization = polarization
        self.phase_init = phase_init

    @cached_property
    def get_omega(self) -> float | complex:
        return self.omega

    @cached_property
    def get_unit_energy_oscillation(self) -> ndarray:
        return self.polarization

    @cached_property
    def get_phase_init(self) -> float:
        return self.phase_init

    @cached_property
    def get_k(self) -> ndarray:
        return self.k


@dataclass
class WaveMode:
    k: ndarray
    vp: float | complex
    polarization: ndarray

    def to_planar_wave(self) -> NumericalPlanarWaveOrInstab:
        return NumericalPlanarWaveOrInstab(
            self.k, self.vp * self.k, self.polarization
        )


class NumericalWaveProblem:
    def get_matrix_big_a(self, k: ndarray) -> ndarray:
        ...

    def get_modes(self, k: ndarray) -> List[WaveMode]:
        the_a = self.get_matrix_big_a
        eig_val, eig_vec_per_column = eig(the_a)
        return [
            WaveMode(k, lambda_i, r_i)
            for lambda_i, r_i in zip(eig_val, eig_vec_per_column.transpose)
        ]
