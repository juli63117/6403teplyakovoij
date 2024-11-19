import pandas as pd
import logging
import logging.config
from pytrends.request import TrendReq

class GoogleTrendsLoader:
    def __init__(self, kw_list, timeframe='today 12-m', config_path='configs/logging.conf'):
        """Инициализация параметров поиска."""
        if isinstance(kw_list, str):
            kw_list = [kw_list]
        self.kw_list = kw_list
        self.timeframe = timeframe
        logging.config.fileConfig(config_path)
        self.logger = logging.getLogger("loader")
        self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)

    def get_trend_data(self):
        """Получает данные о трендах для заданного ключевого слова."""
        try:
            self.pytrends.build_payload(self.kw_list, cat=0, timeframe=self.timeframe, geo='', gprop='')
            data = self.pytrends.interest_over_time()
            if data.empty:
                self.logger.warning("No trend data retrieved.")
                return None
            return data
        except Exception as e:
            self.logger.warning(f"An error occurred: {e}")
            return None

    def get_current_trend_data(self):
        """Получает текущие данные о трендах для заданного ключевого слова."""
        try:
            self.pytrends.build_payload(self.kw_list, cat=0, timeframe='now 1-H', geo='', gprop='')
            current_data = self.pytrends.interest_over_time()
            if current_data.empty:
                self.logger.warning("No current data retrieved for the given keyword.")
                return None
            return current_data
        except Exception as e:
            self.logger.warning(f"An error occurred while fetching current trend data: {e}")
            return None
