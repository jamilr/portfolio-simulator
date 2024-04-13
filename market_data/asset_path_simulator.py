import numpy as np

from const import Const


class AssetPricePathSimulator(object):

    def __init__(self):
        pass

    def _geom_bm(self,  s0: float, mu: float, sigma: float, n: int):
        """
        Attempts at generating an asset price path simulation
        using a Geometric Brownian Motion (GBM) of size N
        and a log-normal distribution

        S_t = S_0 exp((mu-sigma^2/2)t + sigma W_t)

        """
        dt = (1/n)**(1/2)
        t = np.linspace(0, 1, n)
        wiener_process = np.cumsum(np.random.normal(mu, sigma, n)) * dt
        exp_path = (mu - (sigma ** 2) / 2) * t + sigma * wiener_process
        price_path = np.round(s0 * np.exp(exp_path), Const.ROUNDING.value)
        return price_path

    def gen(self,  s0_: float, mu_: float, sigma_: float, n_: int):
        return self._geom_bm(s0_, mu_, sigma_, n_)

