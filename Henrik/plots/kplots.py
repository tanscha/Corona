import matplotlib.pyplot as plt
import numpy as np
import datetime
import xlrd
import time

list = [0.02187380378624816,
        0.02180667675631906,
        0.020236188419550934,
        0.018846312048619612,
        0.017869251985109465,
        0.01746302524257398,
        0.017216974112609834,
        0.0170680615003844]

months = ["JAN", "FEB", "MAR", "APR", "MAI", "JUN", "JUL", "AUG"]

def plotKperMonth():
        plt.plot(months, list, 'rx')
        plt.title("K for hver måned i 2021")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
        plotKperMonth()