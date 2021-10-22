import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlrd
import time

# Spesifiserer hvilke filer som vi henter data fra

locD = pd.read_excel("excel/Covid_deaths.xls")
locI = pd.read_excel("excel/Covid_innlagt.xls")

days = []
innlagt = []
deaths = []


# ----------- Metoder som henter data fra excel-ark START------------
def getDate(c, day, sheet):
    dayvalue = sheet.iloc[day, c]
    print(dayvalue)
    #datetimeobj = datetime.datetime.fromtimestamp(dayvalue)

    #print(dayvalue)
    #y = dayvalue.split(" ")
    #x = y[0].split("-")
    #date = datetime.date(int(x[0]), int(x[1]), int(x[2]))
    date_time = dayvalue.strftime('%d/%m/%Y')
    return date_time

# ----------- Metoder som henter data fra excel-ark SLUTT------------

def D(t):
    xvektor = np.array(locD.iloc[:, 3])
    yvektor = np.array(locD.iloc[:, 2])
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


def K(t):
    xvektor = np.array(locI.iloc[:, 4])
    yvektor = np.array(locI.iloc[:, 3])
    if (t < 0).all():
        print('x kan ikke være mindre enn ' + str(np.min(xvektor)))

    return np.interp(np.array(t), xvektor, yvektor)


# Metode som setter opp funksjonen for C(k, d)
def C(vektor, k, d, T):
    kVektor = k * K(vektor - d)
    dVektor = D(vektor)
    return (np.trapz((kVektor - dVektor) ** 2, vektor)) / (T - d)

def partialDerivK(t, k, d, T, h):
    return (C(t, k+h, d, T)-C(t, k-h, d , T)) / (2*h)


def partialDerivD(t, k, d, T, h):
    return (C(t, k, d+h, T)-C(t, k, d-h, T)) / (2*h)


def plotSteepestDescent(t, periode, start, slutt):
    gammk = 0.000000001
    gammd = 0.01
    hk = 0.1
    hd = 0.1
    Cg = 6000
    Cny = 7000
    k = 0.02
    d = 10
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
    #plt.xlabel("Døgn (" + str(getDate(0, start, locD)) + "-" + str(getDate(0, slutt, locD) + ")"))
    plt.legend(['D(t)', 'k*K(t-d)'])
    plt.title('k: ' + str(k) + '\nd: ' + str(d) + '\nC: ' + str(Cny) + '\niterasjoner: ' + str(iter))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    start_time = time.time()
    start = 0
    slutt = 315
    vektor = np.linspace(start, slutt, (slutt-start))
    plotSteepestDescent(vektor, slutt-start, start, slutt)

    print("--- %s seconds ---" % (time.time()-start_time))