import numpy as np
import pandas as pd

def get_z_score(X):
    mean = np.mean(X)
    std = np.std(X)

    z_score = (X - mean) / std
    
    return z_score
    
def find_outliers(X, threshold = 3, split = 1):
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

    gen.draw_data(data, 1, outliers)

