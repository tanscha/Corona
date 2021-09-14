from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import numpy as np
import pandas as pd

data = pd.read_excel('data.xlsx')


def interpolering_d(t):
    xvektor = np.array(data.iloc[:, 0])
    yvektor = np.array(data.iloc[:, 1])
    if (t < np.min(xvektor)).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))
    elif (t > np.max(xvektor)).all():
        print('x kan ikke være større enn ' + str(np.max(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)



def interpolering_k(t):
    xvektor = np.array(data.iloc[:, 0])
    yvektor = np.array(np.cumsum(data.iloc[:, 3]))
    if (t < np.min(xvektor)).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))
    elif (t > np.max(xvektor)).all():
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
    vektor = np.array(np.linspace(d, 310, 10000))
    kvektor = k * interpolering_k(vektor - d)
    dvektor = interpolering_d(vektor)


    return (np.trapz(vektor, (kvektor - dvektor) ** 2))/(365 - d)



def plot_cost_function():
    n = 400
    # plotvektor = np.array(np.linspace(0, 365, n))
    # plt.plot(plotvektor, interpolering_d(plotvektor))
    # plt.plot(plotvektor, interpolering_k(plotvektor))
    # plt.xlabel('x')
    # plt.show()

    dvektor = np.array(np.linspace(0, 10, 800))
    kvektor = np.array(np.linspace(0, 10, 800))

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

    c_min = 10000
    for k in kvektor:
        for d in dvektor:
            c = cost_function(k, d)
            print(c)
            if c < c_min:
                c_min = c
                k_min = k
                d_min = d

    print(k_min)
    print(d_min)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.plot_trisurf(kvektor, dvektor, cost_matrise, rstride=1, cstride=1, antialiased=True)
    # plt.title('C(k,d)')
    # plt.xlabel('k')
    # plt.ylabel('d')
    # plt.show()

    # fig2 = plt.figure()
    # kvektor, dvektor = np.meshgrid(kvektor, dvektor)
    # plt.pcolor(kvektor, dvektor, np.log(cost_matrise))
    # colorbar()
    # plt.title('ln C(k,d)')
    # plt.xlabel('k')
    # plt.ylabel('d')
    # plt.show()

    plotvektor = np.array(np.linspace(d_min, 310, n))
    plt.plot(plotvektor, np.array(float(k_min) * interpolering_k(plotvektor - float(d_min))))
    plt.plot(plotvektor, interpolering_d(plotvektor))
    plt.xlabel('plotvektor')
    plt.show()


if __name__ == '__main__':
    plot_cost_function()
