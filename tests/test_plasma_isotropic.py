import pytest

from wave_instab_showcase.physics.plasma_isotropic import IsotropicPlasma


def test_default_plasma():
    the_plasma = IsotropicPlasma()
    assert the_plasma.b0_norm == 1.0
    assert the_plasma.f_get_va == 1.0
    assert the_plasma.f_get_cs == (5.0 / 3.0) ** 0.5
