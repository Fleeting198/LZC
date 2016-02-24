import pandas as pd, numpy as np
from pandas import Series, DataFrame

rng = pd.date_range('2015-01-05', periods=500, freq='8h')
ts = pd.Series(np.random.randint(0,500,len(rng)), index=rng)
print ts

print ts.resample('1D', how='sum')

