import unittest

from portfolio_calc.portfolio_state import PortfolioState


class PortfolioStateTest(unittest.TestCase):
    TICKERS = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

    def setUp(self) -> None:
        positions = {ticker: 100*(idx+1) for idx, ticker in enumerate(self.TICKERS)}
        self._state = PortfolioState('TECH', positions)

    def test_default_state(self):
        portfolio = self._state
        result = portfolio.re_price()
        self.assertFalse(result.re_priced)
        self.assertIsNone(portfolio.price)

    def test_update_with_missing_prices(self):
        state = self._state
        results = [state.update(ticker, 100) for ticker in self.TICKERS[:-1]]
        self.assertTrue([r.re_priced is False for r in results[:-1]])

    def test_update_with_all_known_prices(self):
        state = self._state
        results = [state.update(ticker, 100) for ticker in self.TICKERS]
        self.assertTrue([r.re_priced is False for r in results])
        self.assertTrue(results[-1].re_priced)
        self.assertIsNotNone(state.price)
        self.assertEqual(state.price, 100000)

    def test_portfolio_price_changes_with_new_market_data(self):
        state = self._state
        results = [state.update(ticker, 100) for ticker in self.TICKERS]
        self.assertTrue([r.re_priced is False for r in results])
        self.assertTrue(results[-1].re_priced)
        self.assertIsNotNone(state.price)
        self.assertEqual(state.price, 100000)
        old_price = state.price
        result = state.update(self.TICKERS[0], 200)
        self.assertTrue(result.re_priced)
        self.assertEqual(state.price, 110000)
        self.assertNotEqual(state.price, old_price)


if __name__ == '__main__':
    unittest.main()