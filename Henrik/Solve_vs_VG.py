import numpy as np
import xlrd
import matplotlib.pyplot as plt

loc = "Covid_deaths.xls"
loc2 = "Covid_innlagt.xls"
loc3 = "data.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

wb2 = xlrd.open_workbook(loc2)
sheet2 = wb2.sheet_by_index(0)
sheet2.cell_value(0, 0)

wb3 = xlrd.open_workbook(loc3)
sheet3 = wb3.sheet_by_index(0)
sheet3.cell_value(0, 0)

print(sheet.nrows)

days = []
daysSolve = []
solveDeaths = []
solveInnlagte =[]


def getDødsfallNum(i, c, sheet):
    positiv = int(sheet.cell_value(i, c))
    return positiv


def getInnlagtNum(i, c, sheet):
    positiv = int(sheet.cell_value(i, c))
    return positiv


def getDaysInnlagte():
    for i in range(566):
        if i < 1:
            print(i)
        else:
            days.append(i)


def getDaysDøde():
    for i in range(566):
        if i < 1:
            print(i)
        else:
            days.append(i)

def getDaysSolve():
    for i in range(393):
        daysSolve.append(i)


def getInnlagte(column):
    innlagt = []
    for i in range(566):
        if i < 1:
            print(i)
        else:
            innlagt.append(getInnlagtNum(i, column, sheet2))

    return innlagt


def getDødsfall(column):
    deaths = []
    for i in range(566):
        if i < 1:
            print(i)
        else:
            deaths.append(getDødsfallNum(i, column, sheet))

    return deaths

def getSolve(columnD, columnI):
    for i in range(393):
        solveDeaths.append(getDødsfallNum(i, columnD, sheet3))
        solveInnlagte.append(getInnlagtNum(i, columnI, sheet3))

def getInterpSolveInnlagt(vektor):
    return np.interp(vektor, daysSolve, solveInnlagte )


def getInterpSolveDeaths(vektor):
    return np.interp(vektor, daysSolve, solveDeaths)



def plotting():
    getDaysInnlagte()
    getDaysSolve()
    getSolve(1, 2)
    kuminnlagt = getInnlagte(3)

    kumdeaths = getDødsfall(2)

    plot1 = plt.figure(1)

    plt.plot(days, getInterpSolveDeaths(np.array(np.linspace(0, 393, 565))), 'r-', markersize=0.1)

    plt.plot(days, kumdeaths, 'b-', markersize=0.1)

    plot2 = plt.figure(2)
    plt.plot(days, getInterpSolveInnlagt(np.array(np.linspace(0, 393, 565))), 'r-')

    plt.plot(days, kuminnlagt, 'b-')

    plt.show()


if __name__ == "__main__":
    plotting()
