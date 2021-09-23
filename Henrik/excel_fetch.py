import xlrd
import matplotlib.pyplot as plt

loc = "antall_personer_testet.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

print(sheet.nrows)


def main():
    rows = [sheet.nrows]
    sheet.cell_value(2, 0)
    for i in range(sheet.nrows):
        if i == 0 or i == 1:
            print(sheet.cell_value(i, 0) + "\t" + str(sheet.cell_value(i, 1)) + "\t" + str(
                sheet.cell_value(i, 2)) + "\t" + str(sheet.cell_value(i, 3)) + "\t" + "Forskjell")
        else:
            diff = enkelregning(i, 1, 2)
            print(sheet.cell_value(i, 0) + "\t" + str(sheet.cell_value(i, 1)) + "\t" + str(
                sheet.cell_value(i, 2)) + "\t\t" + str(sheet.cell_value(i, 3)) + "\t\t" + str(diff))


def enkelregning(r, c1, c2):
    tall = int(sheet.cell_value(r, c1)) - int(sheet.cell_value(r, c2))
    return tall

def hentTall(i, c):
    positiv = int(sheet.cell_value(i, c))
    return positiv

def plotPos():
    for i in range(sheet.nrows):
        if i < 2:
            print(i)
        else:
            plt.plot([i], [hentTall(i, 2)], 'r.')

    plt.show()

def plotNeg():
    for i in range(sheet.nrows):
        if i < 2:
            print(i)
        else:
            plt.plot([i], [hentTall(i, 1)], 'r.')

    plt.show()

if __name__ == "__main__":
    # main()
    plotPos()
    plotNeg()
