import matplotlib.pyplot as plt
import numpy
import xlrd
from scipy import interpolate
import dødsfall

f2 = 0

deaths = dødsfall.getNumbers(2)

loc = "excel/Covid_deaths.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

days = []

def getDays():
    for i in range(sheet.nrows):
        if i < 1:
            print(i)
        else:
            days.append(i)

def getInterpDeaths(t):
    getDays()

    D = interpolate.interp1d(days, deaths, kind='cubic')
    print(D(19))

    plt.plot(days, deaths, 'r-', markersize=1)

    plt.show()

    return D

if __name__ == "__main__":
    xnew = numpy.linspace(1, 565, 2260)

    getInterpDeaths(xnew)
