import matplotlib.pyplot as plt
import numpy
import xlrd
from scipy import interpolate
import pasienter_innlagt

loc = "excel/Covid_innlagt.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
innlagt = pasienter_innlagt.getNumbers(3)

days = []

def getDays():
    for i in range(sheet.nrows):
        if i < 1:
            print(i)
        else:
            days.append(i)

def getInterpInnlagt():
    getDays()
    K = interpolate.interp1d(days, innlagt, kind='cubic')

    plt.plot(days, innlagt, 'b-', markersize=2)

    plt.show()
    return K


if __name__ == "__main__":
    xnew = numpy.linspace(1, 565, 2260)
    getInterpInnlagt()