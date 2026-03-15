import numpy as np
import pandas as pd

def get_z_score(X: np.ndarray) -> np.ndarray:
    """
    Генерирует Z-Score из массива данных.\n
    Получает: X - Данные\n
    Возвращает: Z-Score\n
    """

    mean = np.mean(X)
    std = np.std(X)

    z_score = (X - mean) / std
    
    return z_score
    
def find_outliers(X: np.ndarray, threshold:float = 3.0, split:int = 1) -> np.ndarray:
    """
    Находит выбросы в массиве данных с помощью метода "3-х Сигм" (Z-Score)\n
    Получает:\n
        X - Данные\n
        threshold - Значение Сигма\n
        split - Разбиение массива данных\n
    Возвращает:\n
        Маску выбросов\n
    """

    pl = len(X) // split
    outliers = X != X
    for i in range(split):
        if i == split - 1:
            z_score = get_z_score(X[i * pl:])
        else:
            z_score = get_z_score(X[i * pl: (i + 1) * pl])

        low = z_score < -threshold
        high = z_score > threshold
        outliers[i * pl : i * pl + len(z_score)] |= low | high

    return outliers

if __name__ == '__main__':
    import generator as gen
    import matplotlib.pyplot as plt

    data = gen.get_data(func={"type":"linear","args":[2,0]},length=100,scaling=10,mode_noise=2,strength=1.5,sleek=100,mode_miss=11,count=1,seed_noise=111,seed_miss=993)
    dataline = data["dataline_miss"]

    outliers = find_outliers(dataline, threshold=3, split=5)
    print(type(outliers))
    gen.draw_data(data, 1, outliers)

