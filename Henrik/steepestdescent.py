from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import numpy as np
import pandas as pd

dataD = pd.read_excel('excel/Covid_deaths.xls')
dataInn = pd.read_excel('excel/Covid_innlagt.xls')


def interpolering_d(t):
    xvektor = np.array(dataD.iloc[:, 3])
    yvektor = np.array(dataD.iloc[:, 2])
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def interpolering_k(t):
    xvektor = np.array(dataInn.iloc[:, 4])
    yvektor = np.array(np.cumsum(dataInn.iloc[:, 1]))
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)

def cost_function(k, d, periode):
    vektor = np.linspace(0, periode , 800)
    kvektor = k * interpolering_k((vektor-d))
    dvektor = interpolering_d(vektor)

    cost = (np.trapz((kvektor - dvektor) ** 2, vektor))/(periode-d)

    return cost


def plot_cost_function(vektor, periode, iterasjoner, start, slutt):
    gamm = 0.000000001
    hd = 0.1
    hk = 0.1
    C = 6000
    Cny = 7000
    k = 0.02
    d = 4.5
    iter=0

    while np.abs(Cny-C) > 1e-6:
        print('while')
        C = Cny
        cdx = (cost_function(k+hk, d, periode) - cost_function(k-hk, d, periode))/(2*hk)
        cdy = (cost_function(k, d+hd, periode) - cost_function(k, d-hd, periode))/(2*hd)
        k = k - gamm*cdx
        print('k: ', k)
        d = d - gamm*cdy
        print('d: ', d)
        Cny = cost_function(k, d, periode)
        print('C: ', Cny)
        iter = iter + 1

    print('iterasjoner: ', iter)
    print(k, d)
    plt.plot(vektor, np.array(k * interpolering_k(vektor - d)))
    plt.plot(vektor, interpolering_d(vektor))
    plt.xlabel('Døgn')
    plt.legend(['k*K(t-d)', 'D(t)'])
    plt.title('k: '+ str(k) + '\nd: ' + str(d) + '\niterasjoner: ' + str(iter))
    plt.tight_layout()
    plt.show()
    print('ferdig')


if __name__ == '__main__':
    start = 316
    slutt = 565
    periode = slutt - start + 1
    iterasjoner = periode * 6
    plotvektor = np.array(np.linspace(0, periode, iterasjoner))
    #steepest_descent()
    plot_cost_function(plotvektor, periode, iterasjoner, start, slutt)
    print(dataD)
    print(dataInn)
