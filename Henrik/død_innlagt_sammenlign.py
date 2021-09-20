import xlrd
import matplotlib.pyplot as plt

loc = "Covid_deaths.xls"

loc2 = "Covid_innlagt.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

wb2 = xlrd.open_workbook(loc2)
sheet2 = wb2.sheet_by_index(0)
sheet2.cell_value(0, 0)

print(sheet.nrows)

days = []

def plotSettings(fig, ax1, ax2, ax1xlabel, ax1ylabel, ax2xlabel):
    fig.tight_layout()
    ax1.set_ylabel(ax1ylabel)
    ax1.set_xlabel(ax1xlabel)
    ax2.set_ylabel(ax2xlabel)
    ax1.yaxis.label.set_color('r')
    ax2.yaxis.label.set_color('b')
    plt.tight_layout()
    plt.show()


def getDødsfallNum(i, c):
    positiv = int(sheet.cell_value(i, c))
    return positiv


def getInnlagtNum(i, c):
    positiv = int(sheet2.cell_value(i, c))
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


def getInnlagte(column):
    innlagt = []
    for i in range(566):
        if i < 1:
            print(i)
        else:
            innlagt.append(getInnlagtNum(i, column))

    return innlagt


def getDødsfall(column):
    deaths = []
    for i in range(566):
        if i < 1:
            print(i)
        else:
            deaths.append(getDødsfallNum(i, column))

    return deaths


def plotting():
    fig, ax1 = plt.subplots()
    getDaysInnlagte()
    kuminnlagt = getInnlagte(3)

    kumdeaths = getDødsfall(2)

    ax1.plot(days, kuminnlagt, 'r-', markersize=0.1)

    ax2 = ax1.twinx()

    ax2.plot(days, kumdeaths, 'b-', markersize=0.1)

    for i_x, i_y in zip(days,
                        kuminnlagt):  # hentet fra https://stackoverflow.com/questions/52408274/showing-points-coordinate-in-plot-in-python
        if i_x == 565:
            ax1.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

    for i_x, i_y in zip(days,
                        kumdeaths):  # hentet fra https://stackoverflow.com/questions/52408274/showing-points-coordinate-in-plot-in-python
        if i_x == 565:
            ax2.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

    plotSettings(fig, ax1, ax2, 'Døgn', 'Innlagte', 'Døde')

    #plt.xlabel("Døgn (21.02.2020 - 07.09.2021)")
    #plt.ylabel("Kumulativ innlagte (rød) vs døde (blå)")

    #plt.show()


if __name__ == "__main__":
    plotting()
