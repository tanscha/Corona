import xlrd
import matplotlib.pyplot as plt

loc = "Covid_innlagt.xls"

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
        if i < 1:
            print(i)
        else:
            days.append(i)


def getNumbers(column):
    innlagt = []
    for i in range(sheet.nrows):
        if i < 1:
            print(i)
        else:
            innlagt.append(getNum(i, column))

    return innlagt


def plotting():
    fig, ax1 = plt.subplots()
    getDays()
    innlagte = getNumbers(1)

    ax1.plot(days, innlagte, 'r-', markersize=0.1)

    ax2 = ax1.twinx()

    innlagte = getNumbers(3)

    ax2.plot(days, innlagte, 'b-', markersize=0.1)

    plotSettings(fig, ax1, ax2, 'Døgn', 'Innlagt per døgn', 'Kumulativ innlagt')


if __name__ == "__main__":
    plotting()
