import datetime

import matplotlib.pyplot as plt
import numpy as np
import xlrd

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


def partialDerivK(vektor, k, d, T, h):
    return (CFunction(vektor, k+h, d, T)-CFunction(vektor, k-h, d, T))/(2*h)


def partialDerivD(vektor, k, d, T, h):
    return (CFunction(vektor, k, d+h, T)-CFunction(vektor, k, d-h, T))/(2*h)


def plotGradientDescent(vektor, periode, iterasjoner, start, slutt):
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
        cdx = (CFunction(vektor, k+hk, d, periode) - CFunction(vektor, k-hk, d, periode))/(2*hk)
        cdy = (CFunction(vektor, k, d+hd, periode) - CFunction(vektor, k, d-hd, periode))/(2*hd)
        k = k - gamm*cdx
        print('k: ', k)
        d = d - gamm*cdy
        print('d: ', d)
        Cny = CFunction(vektor, k, d, periode)
        print('C: ', Cny)
        iter = iter + 1

    print('iterasjoner: ', iter)
    print(k, d)
    plt.plot(vektor, np.array(k * K(vektor - d)))
    plt.plot(vektor, D(vektor))
    plt.xlabel("Døgn (" + str(getDate(0, start, sheet)) + "-" + str(getDate(0, slutt, sheet) + ")"))
    plt.legend(['k*K(t-d)', 'D(t)'])
    plt.title('k: '+ str(k) + '\nd: ' + str(d) + '\niterasjoner: ' + str(iter))
    plt.tight_layout()
    plt.show()
    print('ferdig')


if __name__ == "__main__":
    # Setter hvilken dag vi ønsker å starte perioden fra
    start = 1

    # Setter hvilken dag vi ønsker å slutte perioden på
    slutt = 100

    # Setter hvor mange dager som dataene blir sett over
    periode = slutt - start + 1

    # Angir hvor mange iterasjoner som jeg ønsker å ha for tidsrommet som blir sett på
    iterasjoner = 565

    # Oppretter en vektor med parameterene som ble opprettet ovenfor
    vektor = np.array(np.linspace(0, periode, iterasjoner))

    # Henter antall dager fra excel ark og legger det i et array
    getDays(start, slutt)

    # Henter antall innlagte (kumulativt) fra excel ark og legger det i et array
    getInnlagt(start, slutt)

    # Henter antall døde (kumulativt) fra excel ark og legger det i et array
    getDeaths(start, slutt)

    # Starter utregningsprosessen og plottingen av dataene
    plotGradientDescent(vektor, periode, iterasjoner, start, slutt)
