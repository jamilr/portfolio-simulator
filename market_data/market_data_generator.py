import logging
import random
from typing import Tuple, Any, List

import pandas as pd

from market_data.asset_path_simulator import AssetPricePathSimulator
from utils import read_csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MarketDataGenerator(object):
    TICKER_CLMN = 'NAME'
    CLOSE_CLMN = 'PRICE'
    MU_CLMN = 'MU'
    SIG_CLMN = 'SIG'
    PERIODS_CLMN = 'N'
    PATH_CLMN = 'PATH'
    COLUMNS = [TICKER_CLMN, CLOSE_CLMN, MU_CLMN, SIG_CLMN, PERIODS_CLMN]
    DTYPES = ['string', 'float32', 'float32', 'float32', 'int32']

    def __init__(self, market_datta_file_: str, output_market_prices_file_: str):
        self._market_data_config_file_path = market_datta_file_
        self._output_market_prices_file_path = output_market_prices_file_
        self._simulator = AssetPricePathSimulator()

    def _load_market_data_configuration(self):
        columns_and_dtypes = {c: d for c, d in zip(self.COLUMNS, self.DTYPES)}
        self._market_data_config = read_csv(self._market_data_config_file_path, self.TICKER_CLMN, columns_and_dtypes)

    def _run_asset_path_simulation(self):
        shape = self._market_data_config.shape
        if not shape[0] or not shape[1]:
            return
        self._asset_paths = pd.DataFrame(self._market_data_config.apply(self._gen_price_path, axis=1, result_type='expand'))

    def _shuffle(self):
        ticker_price_tuples = []
        randomized_columns = random.sample(range(len(self._asset_paths.columns)), k=len(self._asset_paths.columns))
        for col in randomized_columns:
            for ticker in self._asset_paths.index:
                ticker_price_tuples.append((ticker, self._asset_paths[col][ticker]))
        random.shuffle(ticker_price_tuples)
        return ticker_price_tuples

    def _gen_price_path(self, row_):
        return dict(enumerate(self._simulator.gen(row_[0], row_[1], row_[2], int(row_[3]))))

    def _persist_asset_prices(self, prices: List[Tuple[Any, Any]]):
        pd.DataFrame(prices, columns=[self.TICKER_CLMN, self.CLOSE_CLMN])\
            .to_csv(self._output_market_prices_file_path, index=False, header=True, mode='w')

    def generate(self):
        self._load_market_data_configuration()
        self._run_asset_path_simulation()
        return self._shuffle()

    def generate_and_persist(self):
        logger.info(f'Generate market data prices. Persist it into {self._output_market_prices_file_path}')
        self._persist_asset_prices(self.generate())

