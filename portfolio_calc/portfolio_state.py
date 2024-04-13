import logging
from collections import defaultdict
from typing import Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PriceUpdateResult:
    def __init__(self, re_priced_: bool):
        self._re_priced = re_priced_

    @property
    def re_priced(self):
        return self._re_priced


class PortfolioState(object):

    def __init__(self, name_: str, positions: Dict[str, float]):
        self._name = name_
        self._positions = positions
        self._state = defaultdict(float)
        self._calculated_portfolio_price = None

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._calculated_portfolio_price

    def _all_ticker_prices_are_known(self):
        return all(
            [True if ticker in self._state and self._state[ticker] else False for ticker in self._positions.keys()])

    def _re_price(self):
        if self._all_ticker_prices_are_known():
            self._re_calc()
            return PriceUpdateResult(True)
        return PriceUpdateResult(False)

    def _update_state(self, position_key_: str, price_: float):
        if position_key_ not in self._positions:
            return
        self._state[position_key_] = price_
        return self._re_price()

    def _re_calc(self):
        self._calculated_portfolio_price = round(sum(
            self._state[ticker] * multiplier for ticker, multiplier in self._positions.items()), 2)

    def update(self, position_key: str, price_: float) -> PriceUpdateResult:
        return self._update_state(position_key, price_)

    def re_price(self):
        return self._re_price()

