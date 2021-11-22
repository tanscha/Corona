import matplotlib.pyplot as plt
import numpy as np
import datetime
import xlrd
import time
from openpyxl import load_workbook

workbook_name = '../excel/Covid_kdpd.xlsx'
wbdpd = load_workbook(workbook_name)
page = wbdpd.active

locKdpd = '../excel/Covid_kdpd.xls'

wbKdpd = xlrd.open_workbook(locKdpd)
sheetdpd = wbKdpd.sheet_by_index(0)
sheetdpd.cell_value(0, 0)

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
kdpd = []
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
        positiv = float(sheet.cell_value(i, c))
        return positiv


# Metode som legger dataene i lister som brukes for å interpolere D(t) og K(t)
def getNumbers(sheet, column, array):
        for i in range(sheet.nrows):
                array.append(float(getNum(i, column, sheet)))


# Metode som henter innlagte fra excel-dataene innenfor spesifisert periode
def getInnlagt(startrad, sluttrad):
        getNumbers(sheet, 3, innlagt)


# Metode som henter dødsfall fra excel-datatene innenfor spesifisert periode
def getDeaths(startrad, sluttrad):
        getNumbers(sheetD, 2, deaths)

def getKdpd():
        getNumbers(sheetdpd, 0, kdpd)


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

def plotkdpd(t, periode):
        gammk = 1e-9 #1e-12
        gammd = 1e-4
        hk = 1e-3
        hd = 0.1
        Cg = 6000
        Cny = 7000
        k = 0.02
        d = 5
        iter = 0
        printIter = 0

        while np.abs(Cny-Cg) > 0.00001: #0.000001
                Cg = Cny
                cdk = partialDerivK(t, k, d, periode, hk)
                cdd = partialDerivD(t, k, d, periode, hd)
                k = k - gammk*cdk
                d = d - gammd*cdd
                Cny = C(t, k, d , periode)
                printIter+=1
                if printIter == 1000:
                        print('k: '+str(k) + "\td: "+str(d)+"\tC: "+str(Cny))
                        printIter=0
                iter = iter+1
        kdpd.append(k)
        #page.append([k])
        print(f'k = {k}')
        #wbdpd.save(filename=workbook_name)

def plotkdpd2021(t, periode):
        gammk = 1e-12
        gammd = 1e-4
        hk = 1e-3
        hd = 0.1
        Cg = 6000
        Cny = 7000
        k = 0.02
        d = 0
        iter = 0
        printIter = 0

        while np.abs(Cny-Cg) > 0.000001:
                Cg = Cny
                cdk = partialDerivK(t, k, d, periode, hk)
                cdd = partialDerivD(t, k, d, periode, hd)
                k = k - gammk*cdk
                d = d - gammd*cdd
                Cny = C(t, k, d , periode)
                printIter+=1
                if printIter == 1000:
                        print('k: '+str(k) + "\td: "+str(d)+"\tC: "+str(Cny))
                        printIter=0
                iter = iter+1
        kdpd.append(k)
        print(f'k = {k}')


if __name__ == "__main__":
        #findStartDate(sheet)
        #findEndDate(sheet)
        start_time = time.time()
        start = 100
        slutt = 283

        vektor = np.linspace(start, slutt, slutt-start+1)

        getDays(0, 609)
        getInnlagt(0, 609)
        getDeaths(0, 609)

        for i in vektor:
                print(f'i = {i}')
                t = np.linspace(int(i)-1, int(i)+1, 3)
                print(t)
                plotkdpd(t, slutt - start + 1)

        #vektor = np.linspace(0, 325, 325)
        print(kdpd)
        plt.plot(vektor, kdpd, 'b-', markersize=0.1)

        start = 284
        slutt = 608

        kdpd = []
        vektor = np.linspace(start, slutt, slutt-start+1)
        getKdpd()

        # for i in vektor:
        #         print(f'i = {i}')
        #         t = np.linspace(int(i)-1, int(i)+1, 3)
        #         print(t)
        #         plotkdpd2021(t, slutt - start + 1)



        plt.plot(vektor, kdpd, 'b-', markersize=0.1)
        #plt.xlabel('Døgn (01.12.2020-21.10.2021)')
        plt.title('K per døgn (2020-2021)')
        plt.show()


        print("--- %s seconds ---" % (time.time()-start_time))
