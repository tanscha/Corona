from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import numpy as np
import pandas as pd

dataD = pd.read_excel('excel/data.xls')


def interpolering_d(t):
    xvektor = np.array(dataD.iloc[:, 1])
    yvektor = np.array(dataD.iloc[:, 2])
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def interpolering_k(t):
    xvektor = np.array(dataD.iloc[:, 1])
    yvektor = np.array(np.cumsum(dataD.iloc[:, 3]))
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def plott_d():
    xvektor = dataD.iloc[:, 1]
    yvektor = dataD.iloc[:, 2]
    plt.plot(xvektor, yvektor)
    xdata = np.linspace(min(xvektor), max(xvektor), 200)
    ydata = interpolering_d(xdata)
    plt.plot(xdata, ydata)
    plt.show()


def plott_k():
    xvektor = dataD.iloc[:, 1]
    yvektor = dataD.iloc[:, 4]
    plt.plot(xvektor, yvektor)
    xdata = np.linspace(min(xvektor), max(xvektor), 200)
    ydata = interpolering_d(xdata)
    plt.plot(xdata, ydata)
    plt.show()


def cost_function(k, d):
    periode = 365 - 1
    vektor = np.linspace(0, 365, 20000)
    kvektor = k * interpolering_k((vektor-d))
    dvektor = interpolering_d(vektor)

    cost = (np.trapz((kvektor - dvektor) ** 2, vektor))/(periode-d)

    return cost


def plot_cost_function(vektor, periode, iterasjoner, start, slutt):
    # plotvektor = np.array(np.linspace(0, 365, n))
    # plt.plot(plotvektor, interpolering_d(plotvektor))
    # plt.plot(plotvektor, interpolering_k(plotvektor))
    # plt.xlabel('x')
    # plt.show()

    dvektor = np.array(np.linspace(0, 10, 800))
    kvektor = np.array(np.linspace(0, 0.5, 800))

    # lengde_d = max(dvektor.shape)
    # lengde_k = max(kvektor.shape)
    # cost_matrise = np.zeros((lengde_k, lengde_d))

    # k_indeks = 1
    # for k in kvektor:
    #     d_indeks = 1
    #     for d in dvektor:
    #         cost_matrise = np.array(cost_function(k, d))
    #         d_indeks = d_indeks + 1
    #     k_indeks = k_indeks + 1

    # c_min = 70000
    # for k in kvektor:
    #     for d in dvektor:
    #         c = cost_function(k, d, start, slutt, periode)
    #         if c_min > c >= 0:
    #             c_min = c
    #             k_min = k
    #             d_min = d
    #             print(c_min)
    #             print(k_min)
    #             print(d_min)

    # print(k_min)
    # print(d_min)
    gamm = 0.000000001
    gammd=0.01
    hd = 0.1
    hk = 0.1
    C = 6000
    Cny = 7000
    k = 0.02
    d = 10
    iter=0

    while np.abs(Cny-C) > 1e-6:
        print('while')
        C = Cny
        cdx = (cost_function(k+hk, d) - cost_function(k-hk, d))/(2*hk)
        cdy = (cost_function(k, d+hd) - cost_function(k, d-hd))/(2*hd)
        k = k - gamm*cdx
        print('k: ', k)
        d = d - gammd*cdy
        print('d: ', d)
        Cny = cost_function(k, d)
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


# def steepest_descent():
#     gamm = 0.0001
#     h = 1e-4
#     C = 6000
#     Cny = 7000
#     k = 0.1
#     d = 4
#     iter=0
#
#     while np.abs(Cny - C) > 1e-8:
#         print('while')
#         C = Cny
#         cdx = (cost_function(k+h, d) - cost_function(k-h, d))/(2*h)
#         cdy = (cost_function(k, d+h) - cost_function(k, d-h))/(2*h)
#         k = k - gamm*cdx
#         print('k: ', k)
#         d = d - gamm*cdy
#         print('d: ', d)
#         Cny = cost_function(k, d)
#         print('C: ', Cny)


if __name__ == '__main__':
    start = 1
    slutt = 316
    periode = slutt - start + 1
    iterasjoner = periode * 6
    plotvektor = np.array(np.linspace(start, slutt, iterasjoner))
    #steepest_descent()
    plot_cost_function(plotvektor, periode, iterasjoner, start, slutt)
