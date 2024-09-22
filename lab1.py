import pandas as pd
import numpy as np
import argparse

def read_config(file_path: str) -> dict:
    """Считывает параметры из CSV файла
    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        dict: Cловарь с параметрами
    """
    data = pd.read_csv(file_path)
    return {
        'n0': int(data['n0'][0]),
        'h': int(data['h'][0]),
        'nk': int(data['nk'][0]),
        'a': float(data['a'][0]),
        'b': float(data['b'][0]),
        'c': float(data['c'][0])
    }

def y(n0: int, h: int, nk: int, a: float, b: float, c: float) -> None:
    """Вычисляет значение уравнения y(x) = sin^2(ax + b) + cos^2(cx)

    Args:
        n0 (int): Начальное значение диапазона
        nk (int): Конечное значение диапазона
        a (float): Коэффициент
        b (float): Коэффициент
        c (float): Коэффициент
    """
    for x in range(n0, nk, h):
        print(np.sin(a * x + b) ** 2 + np.cos(c * x) ** 2)

def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы cmd
    Returns:
        argparse.Namespace: Объект с аргументами
    """
    parser = argparse.ArgumentParser(description='Вычисление уравнения')
    parser.add_argument('config', type=str, help='C:/labs/6403teplyakovoij/config.csv')
    
    return parser.parse_args()

if __name__ == "__main__":
    # Загрузка данных
    args = parse_arguments()
    config = read_config(args.config)
    
    # Инициализация значений
    n0 = config['n0']
    h = config['h']
    nk = config['nk']
    a = config['a']
    b = config['b']
    c = config['c']

    # Вычисление уравнения (в радианах)
    y(n0, h, nk, a, b, c)