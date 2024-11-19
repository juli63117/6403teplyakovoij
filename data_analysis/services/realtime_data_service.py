import logging
import logging.config
import threading
import time
import pandas as pd
from loader.trends_data_loader import GoogleTrendsLoader
from analysis.search_trends_analysis.analysis import TimeSeriesAnalysis
import numpy as np

class RealtimeMonitoringService:
    def __init__(self, service_id, kw_list, timeframe, config_path='configs/logging.conf'):
        self.service_id = service_id
        self.kw_list = kw_list
        self.timeframe = timeframe
        self.stop_event = threading.Event()
        self.thread = None
        logging.config.fileConfig(config_path)
        self.logger = logging.getLogger(f"service_{self.service_id}")
        self.pytrends = GoogleTrendsLoader(kw_list=["data science"], timeframe='today 12-m', config_path=config_path)

    def start(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        self.logger.info(f"Service {self.service_id} started")

    def stop(self):
        self.stop_event.set()
        self.logger.info(f"Service {self.service_id} stopping")
        if self.thread:
            self.thread.join()
        self.logger.info(f"Service {self.service_id} stopped")

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.load_and_analyze()
            except Exception as e:
                self.logger.exception(f"Service {self.service_id} encountered an error: {e}")
            time.sleep(5)

    def load_and_analyze(self):
        try:
            data = self.pytrends.get_trend_data()
            
            if data is not None and not data.empty:
                data = data.infer_objects(copy=False)
                data.reset_index(inplace=True)
                
                keyword = self.kw_list[0]
                ts_analysis = TimeSeriesAnalysis(data[keyword].to_numpy(), config_path='configs/logging.conf')
                
                # Вызываем функции анализа и сохраняем результаты в текстовый файл
                moving_avg = ts_analysis.calculate_moving_average(window_size=5)
                differential = ts_analysis.calculate_differential()
                autocorr = ts_analysis.calculate_autocorrelation()
                maxima = ts_analysis.find_maxima()
                minima = ts_analysis.find_minima()

                # Сохраняем результаты анализа в текстовый файл
                self.save_result_to_file('date', data['date'])
                self.save_result_to_file('moving_average', moving_avg)
                self.save_result_to_file('differential', differential)
                self.save_result_to_file('autocorrelation', autocorr)
                self.save_result_to_file('maxima', maxima)
                self.save_result_to_file('minima', minima)
                
                self.logger.info(f"Service {self.service_id}: Analysis results saved to file.")
            else:
                self.logger.warning(f"Service {self.service_id}: No data received from Google Trends.")
        except Exception as e:
            self.logger.exception(f"Service {self.service_id}: Error during data loading: {e}")

    def save_result_to_file(self, function_name: str, result: pd.Series) -> None:
        """Сохраняет результаты анализа в текстовый файл."""
        with open(f"analysis_results_{self.service_id}.txt", "a") as file:
            file.write(f"\n\nFunction: {function_name}\n")
            file.write(f"Result:\n{result}\n")
            file.write(f"{'-' * 40}\n")
