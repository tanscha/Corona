import datetime

import matplotlib.pyplot as plt
import numpy as np
import xlrd
import time

# Spesifiserer hvilke filer som vi henter data fra

locD = "excel/data.xls"

wbD = xlrd.open_workbook(locD)
sheetD = wbD.sheet_by_index(0)
sheetD.cell_value(0, 0)

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
    getNumbers(sheetD, 2, innlagt, startrad, sluttrad)


# Metode som henter dødsfall fra excel-datatene innenfor spesifisert periode
def getDeaths(startrad, sluttrad):
    getNumbers(sheetD, 1, deaths, startrad, sluttrad)


# Metode som henter antall dager fra excel-dataene innenfor spesifisert periode
def getDays(startrad, sluttrad):
    for i in range(sheetD.nrows):
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


def plotCostFunction(vektor, periode, iterasjoner, start, slutt):
    # Vektorer med parameterverdier
    global dMin, kMin
    n = 100
    kRange = np.array(np.linspace(0, 0.05, n))
    dRange = np.array(np.linspace(0, 60, n))
    iter = 0

    # Finner minste verdi for C med k og d
    CMin = 1000000
    for k in kRange:
        for d in dRange:
            C = CFunction(vektor, k, d,
                          periode)  # Kaller på funksjonen for C som regner ut eventuelle nye minimums C-er
            if C < CMin:  # Hvis funksjonen får en lavere C angir vi nye C, k og d til de nye verdiene
                CMin = C
                kMin = k
                dMin = d
                print("k: " + str(kMin) + "\td: " + str(dMin) + "\tCMin: " + str(
                    CMin))  # Skriver ut de nye verdiene til terminalen
            iter = iter + 1

    print("Done!")


    plotvektor = np.array(np.linspace(dMin, periode, iterasjoner))
    # Plotter D(t)
    plt.plot(plotvektor, D(plotvektor))
    # Plotter k*K(t-d)
    plt.plot(plotvektor, kMin * K(plotvektor - dMin))

    print("k-verdien som gir minst C(k,d) er " + str(kMin))
    print("d-verdien som gir minst C(k,d) er " + str(dMin))
    plt.title("k = " + str(kMin) + "\nd = " + str(dMin) + "\nCMin = " + str(CMin))
    plt.legend(['D(t)', 'k*K(t-d)'])
    plt.tight_layout()
    plt.show()
    print("iterasjoner: "+str(iter))


if __name__ == "__main__":
    start_time = time.time()
    # Setter hvilken dag vi ønsker å starte perioden fra
    start = 0

    # Setter hvilken dag vi ønsker å slutte perioden på
    slutt = 393

    # Setter hvor mange dager som dataene blir sett over
    periode = slutt - start + 1

    # Angir hvor mange iterasjoner som jeg ønsker å ha for tidsrommet som blir sett på
    iterasjoner = periode * 24

    # Oppretter en vektor med parameterene som ble opprettet ovenfor
    vektor = np.array(np.linspace(0, periode, iterasjoner))

    # Henter antall dager fra excel ark og legger det i et array
    getDays(0, 393)

    # Henter antall innlagte (kumulativt) fra excel ark og legger det i et array
    getInnlagt(0, 393)

    # Henter antall døde (kumulativt) fra excel ark og legger det i et array
    getDeaths(0, 393)

    # Starter utregningsprosessen og plottingen av dataene
    plotCostFunction(vektor, periode, iterasjoner, start, slutt)

    print("-------- %s seconds --------" % (time.time()-start_time))
