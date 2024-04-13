import logging

import argparse

from const import Const
from portfolio_calc.portfolio_config import PortfolioConfig
from portfolio_calc.portfolio_manager import PortfolioManager
from market_data.market_data_generator import MarketDataGenerator
from utils import get_file_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATA_FOLDER = 'data'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

MARKET_DATA = 'm'
PORTFOLIO_CALC = 'p'

MARKET_DATA_CONF_DEFAULT = 'market_data_conf.csv'
PORTFOLIOS_CSV_DEFAULT = 'portfolios.csv'
MARKET_DATA_CSV_DEFAULT = 'prices.csv'
PORTFOLIO_PRICES_CSV_DEFAULT = 'portfolio_prices.csv'


def set_up():
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s -- %(message)s', datefmt=DATE_FORMAT)
    logger.setLevel(logging.DEBUG)


def parse_args():
    logger.info('Parsing input arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', default=PORTFOLIO_CALC,
                        choices=[MARKET_DATA, PORTFOLIO_CALC],
                        help='application to run')
    parser.add_argument('--data_conf', default=MARKET_DATA_CONF_DEFAULT,
                        required=False,
                        help='market data generator configuration file')
    parser.add_argument('--portfolios', default=PORTFOLIOS_CSV_DEFAULT,
                        required=False,
                        help='market data generator configuration CSV file')
    parser.add_argument('--market_data', default=MARKET_DATA_CSV_DEFAULT,
                        required=False,
                        help='market data CSV file')
    parser.add_argument('--portfolio_prices', default=PORTFOLIO_PRICES_CSV_DEFAULT,
                        required=False,
                        help='portfolio prices CSV file')
    parsed_args = parser.parse_args()
    logger.info(f'Arguments: {parsed_args}')
    return parsed_args


def generate_market_data(args):
    logger.info('Initializing market data generation')
    asset_close_file_path = get_file_path(DATA_FOLDER, args.data_conf)
    prices_file_path = get_file_path(DATA_FOLDER, args.market_data)
    generator = MarketDataGenerator(asset_close_file_path, prices_file_path)
    generator.generate_and_persist()


def generate_portfolio_prices(args):
    logger.info('Initializing portfolio prices generation')
    portfolios_file_path = get_file_path(DATA_FOLDER, args.portfolios)
    prices_file_path = get_file_path(DATA_FOLDER, args.market_data)
    portfolio_prices_file_path = get_file_path(DATA_FOLDER, args.portfolio_prices)
    config = PortfolioConfig(portfolios_file_path, prices_file_path, portfolio_prices_file_path, Const.CHUNK_SIZE.value)
    p_manager = PortfolioManager(config)
    p_manager.run()


if __name__ == '__main__':
    set_up()
    cmd_args = parse_args()
    if cmd_args.app == MARKET_DATA:
        generate_market_data(cmd_args)
    else:
        generate_portfolio_prices(cmd_args)

