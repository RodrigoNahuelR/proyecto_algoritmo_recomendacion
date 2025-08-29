import pandas as pd
import numpy as np
from numpy.linalg import norm
df = pd.read_csv("data/dataset.csv")

print(pd.get_dummies(df["category"]))

