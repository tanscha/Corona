import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data.xlsx')
data.columns = ['D', 'S', 'I']


death_rate = []
number_of_days = []
# forenklet funksjon for dødsrate
for i in range(0, len(data)):
    death_rate.append(
        (data['D'].iloc[i] / data['S'].iloc[i]) * 100)
    number_of_days.append(i + 1)

data['death_rate'] = death_rate
data['days'] = number_of_days
data.fillna(0)

print(data)

x = data['days']
y = data['I']
plt.plot(x, y, data['D'])
plt.show()