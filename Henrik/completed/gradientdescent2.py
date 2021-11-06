import matplotlib.pyplot as plt
import numpy as np
import datetime
import xlrd
import time

# Spesifiserer hvilke filer som vi henter data fra

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
start = 0
slutt = 0


# ----------- Metoder som henter data fra excel-ark START------------
def getDate(c, day, sheet):
    dayvalue = sheet.cell_value(day, c)
    y = dayvalue.split("T")
    x = y[0].split("-")
    date = datetime.date(int(x[0]), int(x[1]), int(x[2]))
    date_time = date.strftime('%d/%m/%Y')
    return date_time


def findStartDate(sheet):
    global start
    startdate = input("Hvilken dato ønsker du å starte fra? (format må være dd.mm.yyyy)")
    for i in range(sheet.nrows):
        if sheetD.cell_value(i, 0) == "Date":
            i = 1
        dayvalue = sheet.cell_value(i, 0)
        y = dayvalue.split("T")
        x = y[0].split("-")
        date = x[2] + "."+x[1]+"."+x[0]
        if date == startdate:
            print(date + " = " + str(i))
            start = i
            break
    else:
        print("Ikke gyldig dato!")
        findStartDate(sheet)

def findEndDate(sheet):
    global slutt
    enddate = input("Hvilken dato ønsker du å slutte på? (format må være dd.mm.yyyy)")
    for i in range(sheet.nrows):
        if sheetD.cell_value(i, 0) == "Date":
            i = 1
        dayvalue = sheet.cell_value(i, 0)
        y = dayvalue.split("T")
        x = y[0].split("-")
        date = x[2] + "."+x[1]+"."+x[0]
        if date == enddate:
            print(date + " = " + str(i))
            slutt = i
            break
    else:
        print("Ikke gyldig dato!")
        findEndDate(sheet)


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

def D(t):
    return (np.interp(t, days, deaths))


def K(t):
    return (np.interp(t, days, innlagt))

def C(t, k, d, T):
    kVektor = k * K(t-d)
    dVektor = D(t)
    return (np.trapz((kVektor-dVektor)**2, t))

def partialDerivK(t, k, d, T, h):
    return (C(t, k+h, d, T)-C(t, k-h, d , T)) / (2*h)

def partialDerivD(t, k, d, T, h):
    return (C(t, k, d+h, T)-C(t, k, d-h, T)) / (2*h)

def plotSteepestDescent(t, periode, start, slutt):
    gammk = 1e-12
    gammd = 1e-4
    hk = 1e-3
    hd = 0.1
    Cg = 6000
    Cny = 7000
    k = 0.02
    d = 5
    iter = 0

    while np.abs(Cny-Cg) > 0.000001:
        Cg = Cny
        cdk = partialDerivK(t, k, d, periode, hk)
        cdd = partialDerivD(t, k, d, periode, hd)
        k = k - gammk*cdk
        d = d - gammd*cdd
        Cny = C(t, k, d , periode)
        print('k: '+str(k) + "\td: "+str(d)+"\tC: "+str(Cny))
        iter = iter+1

    print("interasjoner: "+str(iter))
    print(k, d)
    plt.plot(t, D(t))
    plt.plot(t, np.array(k*K(t-d)))
    plt.xlabel("Døgn (" + str(getDate(0, start, sheet)) + "-" + str(getDate(0, slutt, sheet) + ")"))
    plt.legend(['D(t)', 'k*K(t-d)'])
    plt.title('k: ' + str(k) + '\nd: ' + str(d) + '\nC: ' + str(Cny) + '\niterasjoner: ' + str(iter))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    findStartDate(sheet)
    findEndDate(sheet)
    start_time = time.time()

    vektor = np.linspace(start, slutt, (slutt-start)*24)

    getDays(0, 609)
    getInnlagt(0, 609)
    getDeaths(0, 609)

    plotSteepestDescent(vektor, slutt-start+1, start, slutt)

    print("--- %s seconds ---" % (time.time()-start_time))