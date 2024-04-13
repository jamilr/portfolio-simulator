import csv
import logging
from collections import defaultdict
from typing import List, Optional

from portfolio_calc.portfolio_config import PortfolioConfig
from portfolio_calc.portfolio_state import PortfolioState, PriceUpdateResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PortfolioManager(object):

    def __init__(self, portfolio_config: PortfolioConfig):
        self._portfolio_config = portfolio_config
        self._portfolio_states = defaultdict(Optional[PortfolioState])
        self._index = None
        self._init()

    def _init(self):
        self._portfolio_config.init()
        positions = self._portfolio_config.portfolio_positions
        for portfolio_name, positions_map in positions.items():
            self._portfolio_states[portfolio_name] = PortfolioState(portfolio_name, positions_map)
        self._index = self._portfolio_config.index
        self._portfolio_prices_file_handler = open(self._portfolio_config.portfolio_prices_file, mode='w', newline='')
        self._market_prices_file_handler = open(self._portfolio_config.prices_file, mode='r')
        self._csv_writer = csv.writer(self._portfolio_prices_file_handler, delimiter=',')
        _ = self._market_prices_file_handler.readline()

    def _append_ticker_price(self, ticker_or_portfolio_: str, price_: float):
        self._csv_writer.writerow([ticker_or_portfolio_, price_])

    def _update_portfolios(self, portfolio_names: List[str], ticker: str, price: float):
        if not portfolio_names:
            return
        for p_name in portfolio_names:
            p_state = self._portfolio_states[p_name]
            result = p_state.update(ticker, price)
            self._append_on_re_price(result, p_state)
            related = self._index[p_name]
            self._update_portfolios(related, p_state.name, p_state.price)

    def _append_on_re_price(self, update_result_: PriceUpdateResult, portfolio_: PortfolioState):
        if update_result_ and update_result_.re_priced:
            self._append_ticker_price(portfolio_.name, portfolio_.price)

    def _close_files(self):
        self._portfolio_prices_file_handler.close()
        self._market_prices_file_handler.close()

    def run(self):
        logger.info('Processing market prices...')
        while True:
            rows = self._market_prices_file_handler.readlines(self._portfolio_config.chunk_size)
            if not rows:
                logger.info('Reached the of the file. Exiting...')
                break
            logger.info(f'Read the next market prices chunk of {len(rows)} records')
            for row in rows:
                ticker, price_str = row.strip('\n').split(',')
                if ticker not in self._index:
                    logger.warning(f'Unknown ticker in the market price data {ticker}')
                    continue
                price = float(price_str)
                self._append_ticker_price(ticker, price)
                self._update_portfolios(self._index[ticker], ticker, price)
        self._close_files()


