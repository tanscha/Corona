import xlrd
import matplotlib.pyplot as plt

loc = "../excel/Covid__vaksinerte.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

print(sheet.nrows)

days = []


def getNum(i, c):
    positiv = int(sheet.cell_value(i, c))
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
    for i in range(sheet.nrows):
        days.append(i)


def getNumbers(column):
    innlagt = []
    for i in range(sheet.nrows):
        innlagt.append(getNum(i, column))

    return innlagt


def plotting():
    getDays()
    vaccineFirstDose = getNumbers(1)

    plt.plot(days, vaccineFirstDose, 'b-', markersize=0.1)
    plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    plt.ylabel('Vaksinerte (Første dose)')
    plt.show()

    vaccineTotal = getNumbers(2)
    plt.plot(days, vaccineTotal, 'b-', markersize=0.1)
    plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    plt.ylabel('Fullvaksinerte')
    plt.show()

    plt.plot(days, vaccineFirstDose, 'r-', markersize=0.1)
    plt.plot(days, vaccineTotal, 'b-', markersize=0.1)
    plt.legend([ 'Første dose', 'Fullvaksinerte'])
    plt.xlabel('Døgn (01.12.2020-26.10.2021)')
    plt.ylabel('Andel (i prosent) vaksinerte')
    plt.show()



if __name__ == "__main__":
    plotting()
