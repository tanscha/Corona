import numpy as np
import xlrd
import matplotlib.pyplot as plt
import kplotsdpd

loc = "../excel/Covid__vaksinerte.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

locKdpd = '../excel/Covid_kdpd.xls'

wbKdpd = xlrd.open_workbook(locKdpd)
sheetdpd = wbKdpd.sheet_by_index(0)
sheetdpd.cell_value(0, 0)

print(sheet.nrows)

days = []
kdpd = []


def getKdpd():
    getNumbers(sheetdpd, 0, kdpd)

def getNum(sheet, i, c):
    positiv = float(sheet.cell_value(i, c))
    return positiv


def plotSettings(fig, ax1, ax2, ax1xlabel, ax1ylabel, ax2xlabel):
    fig.tight_layout()
    ax1.set_ylabel(ax1ylabel)
    ax1.set_xlabel(ax1xlabel)
    ax2.set_ylabel(ax2xlabel)
    ax1.yaxis.label.set_color('r')
    ax2.yaxis.label.set_color('b')
    plt.tight_layout()
    plt.show()


def getDays():
    for i in range(32,325):
        days.append(i)


def getNumbers(sheet, column, list):
    for i in range(32,325):
        list.append(getNum(sheet, i, column))

    return list


def plotting():
    vaccineFirst = []
    vaccineTotal = []
    getKdpd()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, label='1')

    getDays()
    vaccineFirstDose = getNumbers(sheet, 1, vaccineFirst)

    # plt.plot(days, vaccineFirstDose, 'b-', markersize=0.1)
    # plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    # plt.ylabel('Vaksinerte (Første dose)')
    # plt.show()

    vaccineTotal = getNumbers(sheet, 2, vaccineTotal)
    # plt.plot(days, vaccineTotal, 'b-', markersize=0.1)
    # plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    # plt.ylabel('Fullvaksinerte')
    # plt.show()
    #
    # plt.plot(days, vaccineFirstDose, 'r-', markersize=0.1)
    # plt.plot(days, vaccineTotal, 'b-', markersize=0.1)
    # plt.legend([ 'Første dose', 'Fullvaksinerte'])
    # plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    # plt.ylabel('Andel (i prosent) vaksinerte')
    # plt.show()

    list1 = [0.02187380378624816,
    0.02180667675631906,
    0.020236188419550934,
    0.018846312048619612,
    0.017869251985109465,
    0.01746302524257398,
    0.017216974112609834,
    0.0170680615003844]
    listkdpd = []
    months2 = ["JAN", "FEB", "MAR", "APR",
               "MAI", "JUN", "JUL", "AUG"]
    months1 = [1,2,3,4,5,6,7,8]
    #ax1.plot(days, vaccineFirstDose, 'r-', markersize=0.1)
    ax1.plot(days, vaccineTotal, 'b-', markersize=0.1)
    #plt.legend(['Første dose', 'Fullvaksinerte'])
    plt.legend(['Fullvaksinerte'])
    ax2 = fig.add_subplot(111, label='2', frame_on=False)
    ax2.plot(months2, list1, 'g-', markersize=0.1)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    plt.legend(['k per måned'])
    ax1.set_xlabel('Døgn (01.01.2021-26.10.2021)')
    ax1.set_ylabel('Andel (i prosent) vaksinerte')
    ax2.set_ylabel('k per måned')
    ax2.set_xlabel('Måned (Januar - August)')
    ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_label_position('right')
    ax1.tick_params(axis='y', colors="b")
    ax2.tick_params(axis='x', colors="g")
    ax2.tick_params(axis='y', colors="g")
    ax2.xaxis.label.set_color('g')
    ax1.yaxis.label.set_color('b')
    ax2.yaxis.label.set_color('g')
    ax2.get_xaxis().set_visible(False)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotting()
