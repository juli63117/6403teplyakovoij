import unittest
import numpy as np 
import pandas as pd 
from analysis.search_trends_analysis.analysis import TimeSeriesAnalysis

class TestTimeSeriesAnalysis(unittest.TestCase): 
    """Тестирующий класс для проверки функции класса TimeSeriesAnalysis.

    Args:
        unittest.
    """
    def setUp(self): 
        """Инициализация данных для тестов."""
        self.data = np.array([1, 2, 3, 4, 5]) 
        self.ts_analysis = TimeSeriesAnalysis(self.data) 
 
    def test_calculate_moving_average(self): 
        """Тестирование вычисления скользящего среднего."""
        expected_moving_average = [np.nan, np.nan, 2.0, 3.0, 4.0] 
        result = self.ts_analysis.calculate_moving_average(window_size=3) 
        pd.testing.assert_series_equal(pd.Series(result), pd.Series(expected_moving_average)) 
 
    def test_calculate_differential(self): 
        """Тестирование вычисления разности (дифференциала) временного ряда."""
        expected_differential = [np.nan, 1.0, 1.0, 1.0, 1.0] 
        result = self.ts_analysis.calculate_differential() 
        pd.testing.assert_series_equal(pd.Series(result), pd.Series(expected_differential)) 
 
    def test_find_maxima(self): 
        """Тестирование нахождения максимумов в временном ряде."""
        expected_maxima = [np.nan, np.nan, np.nan, np.nan, np.nan] 
        result = self.ts_analysis.find_maxima() 
        pd.testing.assert_series_equal(pd.Series(result), pd.Series(expected_maxima)) 
 
    def test_find_minima(self): 
        """Тестирование нахождения минимумов в временном ряде."""
        expected_minima = [np.nan, np.nan, np.nan, np.nan, np.nan]
        result = self.ts_analysis.find_minima() 
        pd.testing.assert_series_equal(pd.Series(result), pd.Series(expected_minima)) 
 
    def test_calculate_autocorrelation(self): 
        """Тестирование вычисления автокорреляции временного ряда."""
        expected_autocorrelation = [np.nan, 1.0, 1.0, 1.0, np.nan] 
        result = self.ts_analysis.calculate_autocorrelation()
        pd.testing.assert_series_equal(pd.Series(result), pd.Series(expected_autocorrelation)) 
 
    def test_save_to_dataframe(self): 
        """Тестирование сохранения данных в DataFrame."""
        result = self.ts_analysis.save_to_dataframe(pd.Series([1, 2, 3]), 'Test Column') 
        expected_df = pd.DataFrame({'Test Column': [1, 2, 3]}) 
        pd.testing.assert_frame_equal(result, expected_df) 
 
    def test_get_results(self): 
        """Тестирование получения результатов анализа в виде DataFrame."""
        results_df = self.ts_analysis.get_results() 
        expected_columns = ['Original Data', 'Moving Average', 'Differential', 'Maxima', 'Minima', 'Autocorrelation'] 
        self.assertListEqual(list(results_df.columns), expected_columns) 
 
if __name__ == '__main__': 
    unittest.main()