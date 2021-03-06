import datetime

import matplotlib.pyplot as plt
import matplotlib as cm
import numpy as np
import xlrd
import time

# Spesifiserer hvilke filer som vi henter data fra

locD = "excel/Covid_deaths.xls"

wbD = xlrd.open_workbook(locD)
sheetD = wbD.sheet_by_index(0)
sheetD.cell_value(0, 0)

loc = "excel/Covid_innlagt.xls"
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
    return (np.trapz((kVektor - dVektor) ** 2, vektor)) / (T - d)


def surfacePlot(vektor, periode):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    arrayK = K(vektor)
    arrayD = D(vektor)
    arrayC = CFunction(vektor, K(vektor), D(vektor), periode)
    print(arrayK)
    print(arrayD)
    print(arrayC)


    surf = ax.plot_trisurf(arrayK, arrayD, arrayC, cmap= 'coolwarm',
                           linewidth=0, antialiased=False)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)



if __name__ == "__main__":
    start_time = time.time()
    # Setter hvilken dag vi ønsker å starte perioden fra
    start = 1

    # Setter hvilken dag vi ønsker å slutte perioden på
    slutt = 315

    # Setter hvor mange dager som dataene blir sett over
    periode = slutt - start + 1

    # Angir hvor mange iterasjoner som jeg ønsker å ha for tidsrommet som blir sett på
    iterasjoner = periode

    # Oppretter en vektor med parameterene som ble opprettet ovenfor
    vektor = np.array(np.linspace(start, slutt, iterasjoner))

    # Henter antall dager fra excel ark og legger det i et array
    getDays(start, slutt)

    # Henter antall innlagte (kumulativt) fra excel ark og legger det i et array
    getInnlagt(start, slutt)

    # Henter antall døde (kumulativt) fra excel ark og legger det i et array
    getDeaths(start, slutt)

    # Starter utregningsprosessen og plottingen av dataene
    surfacePlot(vektor, periode)

    print("-------- %s seconds --------" % (time.time()-start_time))
