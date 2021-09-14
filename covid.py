import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data.xlsx')
data.columns = ['Dead', 'S', 'I']


# a = startdag, b = sluttdag, k = forholdstall mellom antall døde og innleggelser,?
def cost_func(a, b, k, f, t, d):
    h = 1 / (b - a)
    for r in range(a, b):
        res = np.sum(((k * f(t - d)) - d(t)) ** 2)
        cost = h * res
        return cost

# cumsum av innlagte:
# print(np.cumsum(data['I']))


death_rate = []
number_of_days = []
# forenklet funksjon for dødsrate basert på smittede
for i in range(0, len(data)):
    death_rate.append(
        (data['Dead'].iloc[i] / data['S'].iloc[i]) * 100)
    number_of_days.append(i + 1)

data['death_rate'] = death_rate
data['days'] = number_of_days
data.fillna(0)

# finner antall nye smittede per dag
new_case = data['S'].copy()
for day in range(1, len(data)):
    new_case.iloc[day] = data['S'].iloc[day] - data['S'].iloc[day - 1]

# finner vekstraten fra nye smittede per dag
growth_rate = data['S'].copy()
for day in range(1, len(data)):
    growth_rate.iloc[day] = (new_case.iloc[day] / data['S'].iloc[day - 1]) * 100

print(data)
x = data['days']
y = data['I']
# plt.plot(x, y, data['Dead'])


fixed_growth_rate = 0.1
prediction = data['S'].copy()
for day in range(len(data), len(data) + 10):
    prediction.loc[day] = prediction.loc[day - 1] * (fixed_growth_rate + 1)

plt.plot(x, y)
plt.show()