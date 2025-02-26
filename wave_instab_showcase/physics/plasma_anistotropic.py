r"""
    Numerical models for anisotropic plasmas.
"""


from wave_instab_showcase.math.vector import schmidt, unit
from wave_instab_showcase.physics.numerical_wave_problem import NumericalWaveProblem
from dataclasses import dataclass
from numpy import ndarray, dot, zeros
from numpy.linalg import norm


@dataclass
class PlasmaInfo:
    beta_para: float
    beta_perp: float
    gamma_para: float
    gamma_perp: float


class TwoComponentAnisotropicPlasma(NumericalWaveProblem):
    N_VAR = 11
    I_RHO, I_V_PARA, I_V2, I_V3, I_B_PARA, I_B2, I_B3, \
        I_P_E_PARA, I_P_I_PARA, I_P_E_PERP, I_P_I_PERP = \
        range(N_VAR)

    def __init__(
            self,
            info_e: PlasmaInfo,
            info_i: PlasmaInfo,
            va: float,
            b0: ndarray):
        self.e = info_e
        self.i = info_i
        self.b0 = b0
        self.b0_norm = norm(b0)
        self.b0va = self.b0_norm * va
        self.b02 = self.b0_norm ** 2
        self.b02va = self.b02 * va
        self.inv_b02va = self.b02va ** -1
        self.inv_b0va = self.b0va ** -1
        self.inv_2b0va = 0.5 * self.inv_b0va
        self.b02_beta_e_para_half = self.b02 * info_e.beta_para * 0.5
        self.b02_beta_i_para_half = self.b02 * info_i.beta_para * 0.5
        self.b02_beta_e_perp_half = self.b02 * info_e.beta_perp * 0.5
        self.b02_beta_i_perp_half = self.b02 * info_i.beta_perp * 0.5
        self.b02_e_beta_gamma_para_half = self.b02_beta_e_para_half * info_e.gamma_para
        self.b02_i_beta_gamma_para_half = self.b02_beta_i_para_half * info_i.gamma_para
        self.b02_e_beta_gamma_perp_half = self.b02_beta_e_perp_half * info_e.gamma_perp
        self.b02_i_beta_gamma_perp_half = self.b02_beta_i_perp_half * info_i.gamma_perp
        self.delta_beta = info_e.beta_para - info_e.beta_perp + info_i.beta_para - info_i.beta_perp
        self.delta_beta_over_2b0va = self.delta_beta * self.inv_2b0va
        self.eb0 = unit(b0)

    def cal_k_para(self, k: ndarray):
        return dot(k, self.eb0)

    def cal_k_perp(self, k: ndarray):
        return norm(schmidt(k, self.eb0))

    def get_matrix_big_a(self, k: ndarray) -> ndarray:
        k_para = self.cal_k_para(k)
        k_perp = self.cal_k_perp(k)
        res = zeros((self.N_VAR, self.N_VAR))
        # delta rho line
        res[self.I_RHO, self.I_V_PARA] = self.b02va * k_para
        res[self.I_RHO, self.I_V2] = self.b02va * k_perp
        # delta v_parallel line
        res[self.I_V_PARA, self.I_B2] = self.delta_beta_over_2b0va * k_perp
        res[self.I_V_PARA, self.I_P_E_PARA] = self.inv_b02va * k_para
        res[self.I_V_PARA, self.I_P_I_PARA] = self.inv_b02va * k_para
        # delta v_2 line
        res[self.I_V2, self.I_B_PARA] = self.inv_b0va * k_perp
        res[self.I_V2, self.I_B2] = (self.delta_beta - 2) * self.inv_2b0va * k_para
        res[self.I_V2, self.I_P_E_PERP] = self.inv_b02va * k_perp
        res[self.I_V2, self.I_P_I_PERP] = self.inv_b02va * k_perp
        # delta v_3 line
        res[self.I_V3, self.I_B3] = (self.delta_beta - 2) * self.inv_2b0va * k_para
        # delta B_parallel line
        res[self.I_B_PARA, self.I_V2] = self.b0_norm * k_perp
        # delta B_2 line
        res[self.I_B2, self.I_V2] = -self.b0_norm * k_para
        # delta B_3 line
        res[self.I_B3, self.I_V3] = -self.b0_norm * k_para
        # delta p e parallel line
        res[self.I_P_E_PARA, self.I_RHO] = self.b02_e_beta_gamma_para_half * k_para
        res[self.I_P_E_PARA, self.I_V_PARA] = self.b02_beta_e_para_half * k_para
        # delta p e prep line
        res[self.I_P_E_PERP, self.I_RHO] = self.b02_e_beta_gamma_perp_half * k_perp
        res[self.I_P_E_PERP, self.I_V_PARA] = self.b02_beta_e_perp_half * k_perp
        # delta p i parallel line
        res[self.I_P_I_PARA, self.I_RHO] = self.b02_i_beta_gamma_para_half * k_para
        res[self.I_P_I_PARA, self.I_V_PARA] = self.b02_beta_i_para_half * k_para
        # delta p i prep line
        res[self.I_P_I_PERP, self.I_RHO] = self.b02_i_beta_gamma_perp_half * k_perp
        res[self.I_P_I_PERP, self.I_V_PARA] = self.b02_beta_i_perp_half * k_perp
        return res
