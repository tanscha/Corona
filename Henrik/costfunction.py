import matplotlib.pyplot as plt
import numpy
import numpy as np
import xlrd

import interpolation_innlagt
import interpolation_deaths

loc1 = "excel/Covid_innlagt.xls"

wb1 = xlrd.open_workbook(loc1)
sheet1 = wb1.sheet_by_index(0)
sheet1.cell_value(0, 0)

loc2 = "Covid_deaths.xls"

wb2 = xlrd.open_workbook(loc2)
sheet2 = wb2.sheet_by_index(0)
sheet2.cell_value(0, 0)

days = []
innlagt = []
deaths = []

def getDays():
    for i in range(sheet1.nrows):
        if i < 1:
            print(i)
        else:
            days.append(i)


def getNum(i, c, sheet):
    positiv = int(sheet.cell_value(i, c))
    return positiv


def getNumbersInnlagt(column):
    for i in range(sheet1.nrows):
        if i < 1:
            print(i)
        else:
            innlagt.append(getNum(i, column, sheet1))


def getNumbersDeaths(column):
    for i in range(sheet2.nrows):
        if i < 1:
            print(i)
        else:
            deaths.append(getNum(i, column, sheet2))

def costFunction(k_min, t, d):
    xVektor = numpy.array(numpy.linspace(1, 565, 2260))
    interpolation_innlagt.getInterpInnlagt(xVektor-d)
    kFunction = interpolation_innlagt.f2

    interpolation_deaths.getInterpDeaths(xVektor)
    dFunction = interpolation_deaths.f2

    kVektor = k_min*kFunction
    dVektor = dFunction
    return numpy.trapz(t, (kVektor-dVektor)**2)


def getInterpInnlagt(t):
    return numpy.interp(np.array(t), days, innlagt)


def getInterpDeaths(t):
    return numpy.interp(np.array(t), days, deaths)


def plotMinimumCost():
    xVektor = numpy.linspace(1, 565, 2260)
    plt.plot(xVektor, getInterpInnlagt(xVektor))
    plt.plot(xVektor, getInterpDeaths(xVektor))

    plt.xlabel('Days')
    plt.show()

    dVektor = np.linspace(0, 10, 800)
    kVektor = np.linspace(0, 10, 800)

    lengde_d = len(dVektor)
    lengde_k = len(kVektor)

    k_indeks = 1
    for k in kVektor:
        d_indeks = 1
        for d in dVektor:
            d_indeks = d_indeks+1
        k_indeks = k_indeks+1

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    k_min = input('Hvilken k-verdi gir minst C(k, d)?')
    d_min = input('Hvilken d-verdi gir minst C(k, d)?')
    plt.plot(xVektor, np.array(int(k_min)) * getInterpInnlagt(xVektor - int(d_min)))
    plt.xlabel('plotvektor')
    plt.show()


if __name__ == "__main__":
    getDays()
    getNumbersInnlagt(3)
    getNumbersDeaths(2)

    plotMinimumCost()

