from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import numpy as np
import pandas as pd

data = pd.read_excel('data.xlsx')


def interpolering_d(t):
    print('hei spline d')
    xvektor = np.array(data.iloc[:, 0])
    yvektor = np.array(data.iloc[:, 1])
    if (t < np.min(xvektor)).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))
    elif (t > np.max(xvektor)).any():
        print('x kan ikke være større enn ' + str(np.max(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def interpolering_k(t):
    print('hei spline k')
    xvektor = np.array(data.iloc[:, 0])
    yvektor = np.array(np.cumsum(data.iloc[:, 3]))
    if (t < np.min(xvektor)).any():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))
    elif (t > np.max(xvektor)).any():
        print('x kan ikke være større enn ' + str(np.max(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def plott_d():
    print('hei1')
    xvektor = data.iloc[:, 1]
    yvektor = data.iloc[:, 2]
    plt.plot(xvektor, yvektor)
    xdata = np.linspace(min(xvektor), max(xvektor), 200)
    ydata = interpolering_d(xdata)
    plt.plot(xdata, ydata)
    plt.show()


def plott_k():
    print('hei2')
    xvektor = data.iloc[:, 1]
    yvektor = data.iloc[:, 4]
    plt.plot(xvektor, yvektor)
    xdata = np.linspace(min(xvektor), max(xvektor), 200)
    ydata = interpolering_d(xdata)
    plt.plot(xdata, ydata)
    plt.show()


def cost_function(k, d):
    vektor = np.array(np.linspace(0, 300, 800))
    kvektor = k * interpolering_k(vektor - d)
    dvektor = interpolering_d(vektor)

    return np.trapz(vektor, (kvektor - dvektor)**2)


def plot_cost_function():
    print('hei fra plot_cost')
    n = 800
    plotvektor = np.array(np.linspace(0, 300, n))
    plt.plot(plotvektor, interpolering_d(plotvektor))
    plt.plot(plotvektor, interpolering_k(plotvektor))
    plt.xlabel('x')
    plt.legend('D(t)', 'K(t)')
    plt.show()

    dvektor = np.linspace(0, 10, n)
    kvektor = np.linspace(0, 10, n)

    lengde_d = len(dvektor)
    lengde_k = len(kvektor)
    # cost_matrise = np.zeros(lengde_k, lengde_d)

    k_indeks = 1
    for k in kvektor:
        d_indeks = 1
        for d in dvektor:
            # cost_matrise = cost_function(k, d)
            d_indeks = d_indeks + 1
        k_indeks = k_indeks + 1

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(kvektor, dvektor, cost_matrise, rstride=1, cstride=1, antialiased=True)

    k_min = input('Hvilken k-verdi gir minst C(k,d)?')
    d_min = input('Hvilken d-verdi gir minst C(k,d)?')
    plt.plot(plotvektor, np.array(int(k_min) * interpolering_d(plotvektor - int(d_min))))
    plt.xlabel('plotvektor')
    plt.show()


if __name__ == '__main__':
    plot_cost_function()
