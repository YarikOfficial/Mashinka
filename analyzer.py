import numpy as np
import pandas as pd

def get_z_score(X):
    

def find_outliers

if __name__ == '__main__':
    import generator as gen
    import matplotlib.pyplot as plt
    func = {"type":"linear","args":[3,1]}
    N = 10

    dataline,data = gen.np_gen_func_line(func,N,10,False)

    dataline_miss,data = gen.get_mis(dataline,data,11,round(N/10))


    print(dataline)
    mean = np.nanmean(dataline)
    std = np.nanstd(dataline)
    top = mean + std * 3
    bot = mean - std * 3
    print(std, mean)

    plt.plot(dataline)
    plt.axhline(y=top, color='r', linestyle='-')
    plt.axhline(y=bot, color='r', linestyle='-')
    print(data)
    plt.show()
