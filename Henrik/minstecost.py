import matplotlib.pyplot as plt
import numpy as np
import xlrd
from scipy import interpolate

# Spesifiserer hvilke filer som vi henter data fra
from scipy.interpolate import interp1d

locD = "Covid_deaths.xls"

wbD = xlrd.open_workbook(locD)
sheetD = wbD.sheet_by_index(0)
sheetD.cell_value(0, 0)

loc = "Covid_innlagt.xls"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
days = []
innlagt = []
deaths = []

def getDate(c,day, sheet):
    dayvalue = str(sheet.cell_value(day, c))
    return dayvalue



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


# Metode som setter opp C(k, d)
def CFunction(vektor, k, d, T):
    kVektor = k * K(vektor - d)
    dVektor = D(vektor)
    return (np.trapz(vektor, (kVektor - dVektor))**2) / (T - d)


def plotCostFunction(vektor, periode, iterasjoner, start, slutt):
    # Vektorer med parameterverdier
    global dMin, kMin
    n = 800
    kRange = np.array(np.linspace(0, 0.5, n))
    dRange = np.array(np.linspace(0, 4, n))

    # Finner minste verdi for C med k og d
    CMin = 1000000
    for k in kRange:
        for d in dRange:
            C = CFunction(vektor, k, d, periode)
            if C < CMin:
                CMin = C
                kMin = k
                dMin = d
                print("k: " + str(kMin) + "\td: " + str(dMin) + "\tCMin: " + str(CMin))

    print("Done!")

    # Plotter D(t)
    plotvektor = np.array(np.linspace(dMin, periode, iterasjoner))
    plt.plot(plotvektor, D(plotvektor), 'b-')

    print("k-verdien som gir minst C(k,d) er " + str(kMin))
    print("d-verdien som gir minst C(k,d) er " + str(dMin))

    # Plotter k*K(t-d)
    plt.plot(plotvektor, kMin * K(plotvektor - dMin), 'r--')
    plt.title("k: " + str(kMin) + " / d: " + str(dMin) + "/ CMin: " + str(CMin))
    plt.xlabel("Døgn ("+str(getDate(0, start, sheet))+"-"+str(getDate(0, slutt, sheet)+")"))
    plt.legend(['D(t)', 'k*K(t-d)'])
    plt.show()


# Metode som interpolerer data for dødsfall til en kontinuerlig funksjon
def D(t):
    return np.interp(np.array(t), days, deaths)
    #return interp1d(days, deaths, kind = 'cubic')


# Metode som interpolerer data for innlagte til en kontineurlig funksjon
def K(t):
    return np.interp(np.array(t), days, innlagt)
    #return interp1d(days, innlagt, kind = 'cubic')


if __name__ == "__main__":
    # Setter hvilken dag vi ønsker å starte perioden fra
    start = 10
    # Setter hvilken dag vi ønsker å slutte perioden på
    slutt = 101
    periode = slutt - start + 1
    iterasjoner = periode * 6
    vektor = np.array(np.linspace(0, periode, iterasjoner))
    getDays(start, slutt)
    getInnlagt(start, slutt)
    getDeaths(start, slutt)
    plotCostFunction(vektor, periode, iterasjoner, start, slutt)
