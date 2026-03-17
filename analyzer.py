import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def zscore_gen(X: np.ndarray) -> np.ndarray:
    """
    Генерирует Z-Score из массива данных.\n
    Получает: X - Данные\n
    Возвращает: Z-Score\n
    """

    mean = np.mean(X)
    std = np.std(X)

    z_score = (X - mean) / std
    
    return z_score
    
def zscore_find_outliers(X: np.ndarray, threshold:float = 3.0, split:int = 1) -> np.ndarray:
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
            z_score = zscore_gen(X[i * pl:])
        else:
            z_score = zscore_gen(X[i * pl: (i + 1) * pl])

        low = z_score < -threshold
        high = z_score > threshold
        outliers[i * pl : i * pl + len(z_score)] |= low | high

    return outliers

def get_X(data:dict) -> np.ndarray:
    """Возвращает непрерывный массив данных X из *мегасловаря* им. Радомира!"""
    X = data["dataline_miss"]
    X = X.reshape(-1,1)
    return X


def ml_isoforest(X: np.ndarray, contamination:float = 0.001, random_state:int = 42) -> np.ndarray:
    """
    Находит выбросы в массиве данных с помощью метода Isolation Forest\n
    Получает:\n
        X - Данные\n
        contamination - Ожидаемый процент выбросов\n
        random_state - Случайный сид\n
    Возвращает:\n
        Маску выбросов\n
    """

    iso_forest = IsolationForest(contamination=contamination, random_state=random_state)
    outlier_labels = iso_forest.fit_predict(X)

    return outlier_labels == -1

def ml_lof(X: np.ndarray, n_neighbors:int=5) -> np.ndarray:
    """
    Находит выбросы в массиве данных с помощью метода Local Outlier Factor\n
    Получает:\n
        X - Данные\n
        n_neighbors - Количество ближайших соседей для вычисления LOF\n
    Возвращает:\n
        Маску выбросов\n
    """

    lof = LocalOutlierFactor(n_neighbors=n_neighbors)
    outlier_labels = lof.fit_predict(X)

    return outlier_labels == -1


if __name__ == '__main__':
    import generator as gen

    data = gen.get_data(func={"type":"sin","args":[2,50]},length=100,scaling=10,mode_noise=2,strength=0.1,sleek=100,mode_miss=11,count=5,seed_noise=111,seed_miss=993)

    X = get_X(data)
    outliers = ml_isoforest(X, 0.001)
    #outliers = ml_lof(X, 10)

    gen.draw_data(data, 1, outliers)

