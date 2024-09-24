import pandas as pd
import numpy as np
import argparse

def read_config(file_path: str) -> dict:
    """Считывает параметры из CSV файла.
    
    Args:
        file_path (str): Путь к CSV файлу.

    Returns:
        dict: Словарь с параметрами.
    """
    data = pd.read_csv(file_path)
    return {
        'n0': int(data['n0'][0]),
        'h': float(data['h'][0]),
        'nk': int(data['nk'][0]),
        'a': float(data['a'][0]),
        'b': float(data['b'][0]),
        'c': float(data['c'][0])
    }

def func_calculating(n0: int, h: float, nk: int, a: float, b: float, c: float, output_file: str) -> None:
    """Вычисляет значение уравнения y(x) = sin^2(ax + b) + cos^2(cx) по шагу h и записывает результат в файл.

    Args:
        n0 (int): Начальное значение диапазона.
        h (float): Шаг.
        nk (int): Конечное значение диапазона.
        a (float): Коэффициент.
        b (float): Коэффициент.
        c (float): Коэффициент.
        output_file (str): Путь к выходному файлу для записи результатов.
    """
    with open(output_file, 'w') as f:
        x = n0
        while x < nk:
            result = np.sin(a * x + b) ** 2 + np.cos(c * x) ** 2
            f.write(f"{result}\n")
            x += h

def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с аргументами.
    """
    parser = argparse.ArgumentParser(description="Вычисление значений уравнения")

    parser.add_argument('--config', type=str, help='Путь к конфигурационному CSV файлу')
    parser.add_argument('--output', type=str, default='output.txt', help='Путь к выходному файлу для записи результатов')

    parser.add_argument('--n0', type=int, help='Начальное значение диапазона', required=False)
    parser.add_argument('--h', type=float, help='Шаг', required=False)
    parser.add_argument('--nk', type=int, help='Конечное значение диапазона', required=False)
    parser.add_argument('--a', type=float, help='Коэффициент a', required=False)
    parser.add_argument('--b', type=float, help='Коэффициент b', required=False)
    parser.add_argument('--c', type=float, help='Коэффициент c', required=False)

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    
    # Если данные задаются из файла
    if args.config:
        config = read_config(args.config)
        n0 = config.get('n0', args.n0)
        h = config.get('h', args.h)
        nk = config.get('nk', args.nk)
        a = config.get('a', args.a)
        b = config.get('b', args.b)
        c = config.get('c', args.c)
    # Если данные из консоли
    else:
        n0 = args.n0
        h = args.h
        nk = args.nk
        a = args.a
        b = args.b
        c = args.c

    func_calculating(n0, h, nk, a, b, c, args.output)

if __name__ == "__main__":
    main()
