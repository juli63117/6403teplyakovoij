import pandas as pd
import numpy as np
from typing import Any, Callable

def decorator(func: Callable) -> Callable:
    """
    Декоратор, который проверяет, являются ли входные данные числами, и 
    возвращает результат декорируемой функции.

    Этот декоратор не модифицирует поведение декорируемой функции, а просто 
    предоставляет возможность добавить дополнительный код до или после ее вызова.
    В данном случае, он проверяет, являются ли входные данные числами.

    Args:
        func (Callable): Декорируемая функция.

    Returns:
        Callable: Декорированная функция.
    """ 
    def wrapper(self, *args: Any, **kwargs: Any):
        """
        Обертка для декорируемой функции.

        Args:
        *args: Позиционные аргументы, переданные в декорируемую функцию.
        **kwargs: Именованные аргументы, переданные в декорируемую функцию.

        Returns:
        Результат вызова декорируемой функции.
        """
        for arg in args:
            try:
                float(arg)
            except ValueError:
                raise TypeError("Все аргументы должны быть числами")
        for key, value in kwargs.items():
            try:
                float(value)
            except ValueError:
                raise TypeError(f"Значение аргумента '{key}' должно быть числом")
        return func(self, *args, **kwargs)
    return wrapper

class TimeSeriesAnalysis:
    """
    Класс для анализа временных рядов.

    Атрибуты:
        data (pd.Series): Временной ряд в виде pandas Series.

    Методы:
        calculate_moving_average(window_size: int = 3) -> pd.Series:
        Вычисляет скользящее среднее для временного ряда с заданным размером окна.
        moving_average_generator(self, window_size: int = 3):
        Генератор, генерирующий новые данные через функцию calculate_moving_average().
        calculate_differential() -> pd.Series:
        Вычисляет первую разность временного ряда.
        calculate_autocorrelation(lag: int = 1) -> pd.Series:
        Вычисляет автокорреляцию временного ряда для заданного лага.
        find_maxima() -> pd.Series:
        Находит локальные максимумы во временном ряду.
        find_minima() -> pd.Series:
        Находит локальные минимумы во временном ряду.
        get_results() -> pd.DataFrame:
        Возвращает DataFrame с результатами анализа временного ряда.
    """
    def __init__(self, data: np.ndarray) -> None:
        """
        Инициализация класса с временным рядом.

        Аргументы: 
        data (np.ndarray) - массив данных для инициализации временного ряда
        """
        self.data = pd.Series(data)

    @decorator
    def calculate_moving_average(self, window_size: int = 3) -> pd.Series:
        """
        Вычисляет скользящее среднее для временного ряда с заданным размером окна.

        Args:
        window_size (int, optional): Размер окна для скользящего среднего. По умолчанию 3.

        Returns:
        pd.Series: Временной ряд с вычисленным скользящим средним.
        """
        moving_average = [np.nan] * (window_size - 1)
        moving_average.extend(self.data.rolling(window=window_size).mean()[window_size - 1:])
        return pd.Series(moving_average)

    def moving_average_generator(self, window_size: int = 3):
        """Генератор для функции, вычисляющей скользящее среднее.

        Args:
            window_size (int, optional): Размер окна. По умолчанию 3.
        """
        current_index = 0
        moving_average_series = self.calculate_moving_average(window_size)

        while current_index < len(moving_average_series):
            yield moving_average_series.iloc[current_index]
            current_index += 1

    @decorator
    def calculate_differential(self) -> pd.Series:
        """
        Вычисляет первую разность временного ряда.

        Returns:
        pd.Series: Временной ряд с вычисленной первой разностью.
        """
        differential = [np.nan]
        differential.extend(self.data.diff()[1:])
        return differential

    @decorator
    def calculate_autocorrelation(self) -> pd.Series:
        """
        Вычисляет автокорреляцию временного ряда для заданного лага.

        Returns:
        pd.Series: Временной ряд с вычисленной автокорреляцией.
        """
        if len(self.data) < 2:
            return pd.Series([np.nan] * len(self.data))
        autocorr_series = pd.Series(index=self.data.index)
        for lag in range(1, len(self.data)):
            autocorr_series[lag] = self.data.autocorr(lag)

        return autocorr_series

    @decorator
    def find_maxima(self) -> pd.Series:
        """
        Находит локальные максимумы во временном ряду.

        Returns:    
        pd.Series: Временной ряд с найденными локальными максимумами.
        """
        maxima = [np.nan]
        maxima.extend(
            [self.data[i] if (self.data[i - 1] < self.data[i] > self.data[i + 1]) else np.nan 
            for i in range(1, len(self.data) - 1)]
        )
        maxima.append(np.nan)
        return maxima

    @decorator
    def find_minima(self) -> pd.Series:
        """
        Находит локальные минимумы во временном ряду.

        Returns:
            pd.Series: Временной ряд с найденными локальными минимумами.
        """
        minima = [np.nan]
        minima.extend(
            [self.data[i] if (self.data[i - 1] > self.data[i] < self.data[i + 1]) else np.nan 
            for i in range(1, len(self.data) - 1)]
        )
        minima.append(np.nan)
        return minima

    def save_to_dataframe(self, result: pd.Series, name: str) -> pd.DataFrame:
        """
        Сохраняет результат вычислений в DataFrame с заданным именем столбца.

        Аргументы:
        result (pd.Series) - результат вычислений.
        name (str) - имя столбца для результата в DataFrame.

        Возвращает:
        pd.DataFrame - DataFrame с результатами.
        """
        return pd.DataFrame({name: result})

    def get_results(self) -> pd.DataFrame:
        """
        Возвращает DataFrame с результатами анализа временного ряда.

        Returns:
            pd.DataFrame: DataFrame с результатами анализа.
        """
        df = self.save_to_dataframe(self.data, 'Original Data')
        for avg in self.moving_average_generator(window_size=3):
            df['Moving Average'] = list(self.calculate_moving_average())
        df['Differential'] = list(self.calculate_differential())
        df['Maxima'] = list(self.find_maxima())
        df['Minima'] = list(self.find_minima())
        df['Autocorrelation'] = self.calculate_autocorrelation()
        
        return df

    def save_results_to_excel(self, results_df, file_name: str = 'results.xlsx') -> None:
        """
        Сохранение результатов анализа в Excel.
        """
        self.results = results_df
        with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
            self.results.to_excel(writer, index=False)