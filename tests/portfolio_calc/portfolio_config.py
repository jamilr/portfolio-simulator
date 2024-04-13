import unittest

from portfolio_calc.portfolio_config import PortfolioConfig


class PortfolioConfigTest(unittest.TestCase):

    PORTFOLIO_DEF_FILE = '../data/portfolios.csv'
    PORTFOLIO_CONFIG = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.PORTFOLIO_CONFIG = PortfolioConfig(cls.PORTFOLIO_DEF_FILE, '', '', 1000)
        cls.PORTFOLIO_CONFIG.init()

    def test_list_of_portfolio_positions_match_all_portfolios(self):
        positions = self.PORTFOLIO_CONFIG.portfolio_positions
        portfolios = self.PORTFOLIO_CONFIG.portfolios
        self.assertEqual(len(positions.keys()),     len(portfolios))
        self.assertEqual(sorted(positions.keys()),  sorted(portfolios))

    def test_is_able_to_find_portfolio_by_asset_ticker_from_index(self):
        positions = self.PORTFOLIO_CONFIG.portfolio_positions
        for p_name, positions in positions.items():
            for ticker, multiplier in positions.items():
                related_portfolios = self.PORTFOLIO_CONFIG.index[ticker]
                self.assertIsNotNone(related_portfolios)
                self.assertEqual(sorted(related_portfolios), sorted([p_name]))


if __name__ == '__main__':
    unittest.main()