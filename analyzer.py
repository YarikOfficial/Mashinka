import numpy as np
import pandas as pd

def get_z_score(X):
    mean = np.nanmean(X)
    std = np.nanstd(X)

    z_score = (X - mean) / std
    
    return z_score
    
def find_outliers(X, threshold = 3):
    z_score = get_z_score(X)

    low = np.where(z_score < -threshold)[0]
    high = np.where(z_score > threshold)[0]
    outliers = np.concatenate((low, high))

    return outliers

if __name__ == '__main__':
    import generator as gen
    import matplotlib.pyplot as plt

    data = gen.get_data(func={"type":"root","args":[2.6667,0.45,-3.2]},length=100,scaling=10,mode_noise=1,strength=0.1,sleek=10,mode_miss=11,count=10,seed_noise=111,seed_miss=993)
    dataline = data["dataline"]

    outliers = find_outliers(dataline, 1)

    print(outliers, type(outliers))

    gen.draw_data(data, 1)

