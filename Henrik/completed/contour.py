import datetime

import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import re
import numpy as np
import xlrd
import time
from mpl_toolkits.mplot3d import Axes3D

# Spesifiserer hvilke filer som vi henter data fra
import scipy.interpolate as interp

k_column, d_column, c_column = [], [], []
with open('myfile.csv') as f:
    lines = f.readlines()
    for x in lines:
        k_column.append(int(x.split(', ')[0]))
        d_column.append(int(x.split(', ')[1]))
        c_column.append(float(re.split('\n', x.split(', ')[2])[0]))
    k_column = np.array(k_column)
    d_column = np.array(d_column)
    c_column = np.array(c_column)


locD = "../excel/Covid_deaths.xls"

wbD = xlrd.open_workbook(locD)
sheetD = wbD.sheet_by_index(0)
sheetD.cell_value(0, 0)

loc = "../excel/Covid_innlagt.xls"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
days = []
innlagt = []
deaths = []


# ----------- Metoder som henter data fra excel-ark START------------
def getDate(c, day, sheet):
    dayvalue = sheet.cell_value(day, c)
    y = dayvalue.split("T")
    x = y[0].split("-")
    date = datetime.date(int(x[0]), int(x[1]), int(x[2]))
    date_time = date.strftime('%d/%m/%Y')
    return date_time


# Metode som henter data fra hver celle i excel
def getNum(i, c, sheet):
    positiv = int(sheet.cell_value(i, c))
    return positiv


# Metode som legger dataene i lister som brukes for å interpolere D(t) og K(t)
def getNumbers(sheet, column, array, startrad, sluttrad):
    for i in range(sheet.nrows):
        if i < startrad:
            print()
        elif i <= sluttrad:
            array.append(int(getNum(i, column, sheet)))


# Metode som henter innlagte fra excel-dataene innenfor spesifisert periode
def getInnlagt(startrad, sluttrad):
    getNumbers(sheet, 3, innlagt, startrad, sluttrad)


# Metode som henter dødsfall fra excel-datatene innenfor spesifisert periode
def getDeaths(startrad, sluttrad):
    getNumbers(sheetD, 2, deaths, startrad, sluttrad)


# Metode som henter antall dager fra excel-dataene innenfor spesifisert periode
def getDays(startrad, sluttrad):
    for i in range(sheet.nrows):
        if i < startrad:
            print()
        elif i <= sluttrad:
            days.append(i)


# ----------- Metoder som henter data fra excel-ark SLUTT------------


# Metode som interpolerer data for dødsfall til en kontinuerlig funksjon
def D(t):
    return np.interp(np.array(t), days, deaths)


# Metode som interpolerer data for innlagte til en kontinuerlig funksjon
def K(t):
    return np.interp(np.array(t), days, innlagt)


# Metode som setter opp funksjonen for C(k, d)
def CFunction(vektor, k, d, T):
    kVektor = k * K(vektor - d)
    dVektor = D(vektor)
    return (np.trapz((kVektor - dVektor) ** 2, vektor))


def plotCostFunction(vektor, periode, iterasjoner, start, slutt):
    # Vektorer med parameterverdier
    # global dMin, kMin
    # n = 150
    # kRange = np.array(np.linspace(0, 0.03, n))
    # dRange = np.array(np.linspace(0, 5, n))
    # iter = 0
    # Kmatrix, Dmatrix = np.meshgrid(kRange, dRange)
    # Cmatrix = np.array(Kmatrix, Dmatrix)
    # # Finner minste verdi for C med k og d
    # CMin = 1e9
    # kind = 0
    # #file = open("myfile.txt","x")
    # for k in kRange:
    #     dind = 0
    #     for d in dRange:
    #         C = CFunction(vektor, k, d,
    #                       periode)  # Kaller på funksjonen for C som regner ut eventuelle nye minimums C-er
    #         #file.write(f"{kind}, {dind}, {C}\n")
    #         Cmatrix.__add__(C)
    #         dind += 1
    #         iter = iter + 1
    #     kind += 1
    # print("Done!")
    # #file.close()
    # print(Cmatrix)



    #https://stackoverflow.com/questions/35259285/plotting-three-lists-as-a-surface-plot-in-python-using-mplot3d

    plotx,ploty, = np.meshgrid(np.linspace(np.min(k_column),np.max(k_column),22500),
                               np.linspace(np.min(d_column),np.max(d_column),22500))
    plotz = interp.griddata((k_column,d_column),c_column,(plotx,ploty),method='linear')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(plotx,ploty,plotz,cstride=1,rstride=1,cmap='viridis')


    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #ax.plot_trisurf(k_column, d_column, c_column, linewidth=0, antialiased=False)
    plt.show()


if __name__ == "__main__":
    print(f"kcolumn: {k_column.size}")
    print(f"dcolumn: {d_column.size}")
    print(f"ccolumn: {c_column.size}")
    start_time = time.time()
    # Setter hvilken dag vi ønsker å starte perioden fra
    start = 1

    # Setter hvilken dag vi ønsker å slutte perioden på
    slutt = 315

    # Setter hvor mange dager som dataene blir sett over
    periode = slutt - start + 1

    # Angir hvor mange iterasjoner som jeg ønsker å ha for tidsrommet som blir sett på
    iterasjoner = periode * 6

    # Oppretter en vektor med parameterene som ble opprettet ovenfor
    vektor = np.array(np.linspace(start, slutt, iterasjoner))


    # Henter antall dager fra excel ark og legger det i et array
    getDays(start, slutt)

    # Henter antall innlagte (kumulativt) fra excel ark og legger det i et array
    getInnlagt(start, slutt)

    # Henter antall døde (kumulativt) fra excel ark og legger det i et array
    getDeaths(start, slutt)

    # Starter utregningsprosessen og plottingen av dataene
    plotCostFunction(vektor, periode, iterasjoner, start, slutt)

    print("-------- %s seconds --------" % (time.time()-start_time))
