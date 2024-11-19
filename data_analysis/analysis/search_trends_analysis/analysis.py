import pandas as pd 
import numpy as np 
from typing import Any, Callable 
import logging 
import logging.config 

def decorator(func: Callable) -> Callable:
    """
    Декоратор, который проверяет, являются ли входные данные числами,
    и логирует вызовы функции в файл logs/app.log.

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
        # Логируем вызов функции с аргументами, исключая большие структуры данных
        args_str = [str(arg) if not isinstance(arg, (pd.Series, np.ndarray)) else f"<{type(arg).__name__}>" for arg in args]
        kwargs_str = {key: (str(value) if not isinstance(value, (pd.Series, np.ndarray)) else f"<{type(value).__name__}>") for key, value in kwargs.items()}
        
        logging.info(f"Calling {func.__name__} with args={args_str} and kwargs={kwargs_str}")
        
        # Проверяем, что все аргументы являются числами
        for arg in args:
            try:
                float(arg)
            except ValueError:
                error_msg = f"Invalid argument: {arg} is not a number"
                logging.error(error_msg)
                raise TypeError("Все аргументы должны быть числами")
        
        for key, value in kwargs.items():
            try:
                float(value)
            except ValueError:
                error_msg = f"Invalid keyword argument: {key}={value} is not a number"
                logging.error(error_msg)
                raise TypeError(f"Значение аргумента '{key}' должно быть числом")
        
        # Вызов декорируемой функции
        result = func(self, *args, **kwargs)
        
        # Логируем результаты, исключая сами данные
        if isinstance(result, (pd.Series, np.ndarray)):
            logging.info(f"Result of {func.__name__} is a {type(result).__name__}, not logged.")
        else:
            logging.info(f"Result of {func.__name__}: {result}")
        
        return result

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
    """

    def __init__(self, data: np.ndarray, config_path='configs/logging.conf') -> None: 
        """ 
        Инициализация класса с временным рядом.
        """
        logging.config.fileConfig(config_path) 
        self.logger = logging.getLogger("analysis") 
        self.data = pd.Series(data)
    
    @decorator 
    def calculate_moving_average(self, window_size: int = 3) -> pd.Series: 
        """Вычисляет скользящее среднее для временного ряда с заданным размером окна."""
        moving_average = [np.nan] * (window_size - 1) 
        moving_average.extend(self.data.rolling(window=window_size).mean()[window_size - 1:]) 
        return pd.Series(moving_average) 

    def moving_average_generator(self, window_size: int = 3): 
        """Генератор для функции, вычисляющей скользящее среднее."""
        current_index = 0 
        moving_average_series = self.calculate_moving_average(window_size) 
        while current_index < len(moving_average_series): 
            yield moving_average_series.iloc[current_index] 
            current_index += 1 
        self.logger.info(f"Analysis calculated moving average") 

    @decorator 
    def calculate_differential(self) -> pd.Series: 
        """Вычисляет первую разность временного ряда."""
        differential = [np.nan] 
        differential.extend(self.data.diff()[1:]) 
        self.logger.info(f"Analysis calculated differential") 
        return differential 

    @decorator 
    def calculate_autocorrelation(self) -> pd.Series: 
        """Вычисляет автокорреляцию временного ряда для заданного лага."""
        if len(self.data) < 2: 
            return pd.Series([np.nan] * len(self.data)) 
        autocorr_series = pd.Series(index=self.data.index) 
        for lag in range(1, len(self.data)): 
            autocorr_series[lag] = self.data.autocorr(lag) 
        self.logger.info(f"Analysis calculated autocorrelation") 
        return autocorr_series 

    @decorator 
    def find_maxima(self) -> pd.Series: 
        """Находит локальные максимумы во временном ряду."""
        maxima = [np.nan] 
        maxima.extend( 
            [self.data[i] if (self.data[i - 1] < self.data[i] > self.data[i + 1]) else np.nan  
            for i in range(1, len(self.data) - 1)] 
        ) 
        maxima.append(np.nan) 
        self.logger.info(f"Analysis found maxima") 
        return maxima 

    @decorator 
    def find_minima(self) -> pd.Series: 
        """Находит локальные минимумы во временном ряду."""
        minima = [np.nan] 
        minima.extend( 
            [self.data[i] if (self.data[i - 1] > self.data[i] < self.data[i + 1]) else np.nan  
            for i in range(1, len(self.data) - 1)] 
        ) 
        minima.append(np.nan) 
        self.logger.info(f"Analysis found minima") 
        return minima 