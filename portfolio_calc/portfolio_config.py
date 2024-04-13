import csv
from collections import defaultdict
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PortfolioConfig(object):
    NAME_KEY = 'NAME'
    SHARES_KEY = 'SHARES'

    def __init__(self, portfolio_definitions_file: str, prices_file: str, portfolio_prices_file: str, chunk_size_: int):
        self._portfolio_def_file = portfolio_definitions_file
        self._prices_file = prices_file
        self._portfolio_prices_file = portfolio_prices_file
        self._chunk_size_ = chunk_size_
        self._portfolio_names = None
        self._portfolio_positions = None
        self._index = None

    @property
    def portfolio_def_file(self) -> str:
        return self._portfolio_def_file

    @property
    def prices_file(self) -> str:
        return self._prices_file

    @portfolio_def_file.setter
    def portfolio_def_file(self, value:str):
        self._portfolio_def_file = value

    @prices_file.setter
    def prices_file(self, value: str):
        self._prices_file = value

    @property
    def portfolio_prices_file(self) -> str:
        return self._portfolio_prices_file

    @property
    def portfolios(self) -> List[str]:
        return self._portfolio_names

    @property
    def portfolio_positions(self) -> Dict[str, Dict[str, float]]:
        return self._portfolio_positions

    @property
    def index(self) -> Dict[str, List[str]]:
        return self._index

    @property
    def chunk_size(self) -> int:
        return self._chunk_size_

    def _read_csv(self):
        with open(self._portfolio_def_file, mode='r') as file:
            csv_data = csv.DictReader(file)
            if not csv_data:
                return
            for row in csv_data:
                yield row

    def init(self):
        if not self._portfolio_def_file:
            return
        logger.info('Reading portfolio definitions CSV file')
        portfolio_names = []
        cur_portfolio = None
        portfolio_map = defaultdict(dict)
        inverted_index = defaultdict(list)
        for row in self._read_csv():
            if not row[self.SHARES_KEY]:
                cur_portfolio = row[self.NAME_KEY]
                portfolio_names.append(cur_portfolio)
                portfolio_map[cur_portfolio] = dict()
            else:
                ticker_or_portfolio, multiplier = row[self.NAME_KEY], float(row[self.SHARES_KEY])
                if cur_portfolio:
                    inverted_index[ticker_or_portfolio].append(cur_portfolio)
                    portfolio_map[cur_portfolio][ticker_or_portfolio] = multiplier
        self._index = inverted_index
        self._portfolio_positions = portfolio_map
        self._portfolio_names = portfolio_names
        logger.info('Portfolios configuration has been created')




