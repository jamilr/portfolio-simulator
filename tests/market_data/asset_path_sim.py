import unittest

import numpy as np

from market_data.asset_path_simulator import AssetPricePathSimulator


class AssetPricePathSimulationTest(unittest.TestCase):
    S0 = 100.0
    MU = 0.05
    SIGMA = 0.3
    PERIODS = 1000
    SIMULATOR = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.SIMULATOR = AssetPricePathSimulator()

    def test_price_path_size(self):
        path = self.SIMULATOR.gen(self.S0, self.MU, self.SIGMA, self.PERIODS)
        self.assertEqual(path.shape[0], self.PERIODS)

    def test_price_path_follows_normal_distribution(self):
        path = self.SIMULATOR.gen(self.S0, self.MU, self.SIGMA, self.PERIODS)
        mean = np.mean(path)
        std_dev = np.std(path)
        one_std_dev = [True if abs(mean - price) <= std_dev else False for price in path]
        one_std_dev_pcnt = round(len(list(filter(lambda x: x is True, one_std_dev))) / len(one_std_dev), 2) * 100
        self.assertLess(one_std_dev_pcnt, 68.27)


if __name__ == '__main__':
    unittest.main()