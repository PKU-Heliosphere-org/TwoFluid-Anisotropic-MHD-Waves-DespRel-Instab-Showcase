r"""
    Waves.
"""


from numpy import ndarray


class Wave:
    r"""
        Wave features.
    """
    def get_dispersion(self) -> ndarray:
        ...

    def get_unit_energy_oscillation(self) -> ndarray:
        ...
