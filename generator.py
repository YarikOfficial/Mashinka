from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

len = 100

def generate_dataline(len = 10,seed = 993):
    x,y = make_classification(n_samples=1,n_features=len,n_informative=10,n_redundant=2,n_classes=2,random_state=seed)
    dataline = pd.DataFrame(x)
    return dataline

dataline = generate_dataline(len,1)

plt.hist(dataline,bins=len)
plt.show()