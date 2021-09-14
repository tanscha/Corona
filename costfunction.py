import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_excel('data.xlsx')

data.dropna(inplace=True)
data.describe()
data.columns = ['Dead', 'S', 'I']
number_of_days = []
for i in range(0, len(data)):
    number_of_days.append(i + 1)
data['days'] = number_of_days
data.fillna(0)

fig, (ax1) = plt.subplots(1, figsize=(12, 6))
ax1.scatter(y=data['Dead'], x=np.cumsum(data['I']), s=8)
plt.title('Døde vs innlagte')
plt.xlabel('Innlagte')
plt.ylabel('Døde')
plt.show()

y = data['Dead'].values.reshape(-1, 1).astype('float32')
x = np.cumsum(data['I']).values.reshape(-1, 1).astype('float32')

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

h = LinearRegression()
h.fit(x_train, y_train)
print(h.intercept_)
print(h.coef_)

y_pred = h.predict(x_test)
compare = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
compare

fig2, (ax1) = plt.subplots(1, figsize=(12, 6))
ax1.scatter(x_test, y_test, s=8)
plt.plot(x_test, y_pred, color='black', linewidth=2)
plt.show()

theta_0 = np.random.random()
k = np.random.random()


# def hypotese(theta_0, theta_1, x):
# return theta_1*x + theta_0


def cost_function(x, y, theta_0, k):
    m = len(x)
    d = 1
    summation = 0.0
    for j in range(m):
        summation += ((k * x[(j - d)]) - y[j]) ** 2
    return summation / (m - d)


def descent(x, y, theta_0, k, learning_rate):
    t0_deriv = 0
    k_deriv = 0
    m = len(x)
    for j in range(m):
        t0_deriv += (k * x[j] + theta_0) - y[j]
        k_deriv += ((k * x[j] + theta_0) - y[j]) * x[j]

    theta_0 -= (1 / m) * learning_rate * t0_deriv
    k -= (1 / m) * learning_rate * k_deriv

    return theta_0, k


def training(x, y, theta_0, k, learning_rate, iter):
    cost_hist = [0]
    t0_hist = [0]
    k_hist = [0]
    for j in range(iter):
        theta_0, k = descent(x, y, theta_0, k, learning_rate)
        t0_hist.append(theta_0)
        k_hist.append(k)
        cost = cost_function(x, y, theta_0, k)
        cost_hist.append(cost)
        if i % 10 == 0:
            print("iter={}, theta_0={}, theta_1={}, cost={}".format(j, theta_0, k, cost))
    return t0_hist, k_hist, cost_hist


t0_hist, k_hist, cost_hist = training(x, y, theta_0, k, 0.01, 2000)

plt.title('Cost Function')
plt.xlabel('Antall iterasjoner')
plt.ylabel('Cost')
plt.plot(cost_hist)
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.show()


def cost_func(k, d):
    t_vector = np.linspace(0, 365, 365)

    d_vector = d_func(t_vector)
    k_vector = k * k_function(t_vector - d)

    cost = np.trapz(t_vector, (d_vector - k_vector) ** 2)

    return cost


def d_func(t):
    if t == data['days']:
        return data['Dead']


def k_function(t):
    return np.trapz(t, data['I'])
