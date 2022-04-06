import matplotlib.pyplot as plt
from datetime import datetime

def out(name = "default.txt", text = "default text"):
    cur = datetime.now()
    fName = cur.strftime("%m-%d-%y_") + name
    fText = cur.strftime("%H:%M:%S\n") + text

    f = open(fName, "a")
    f.write(fText + "\n\n")
    f.close()

def graph(yp, name):
    if len(yp) > 0:
        print(yp)
        xp, n = [], 0
        for i in yp:
            n += 1
            xp.append(n)
        
        plt.title(name + " Over Time")
        plt.ylabel("Seconds")
        plt.ylim(0, yp[len(yp) - 1])
        plt.xlabel("Reps")
        plt.xlim(0, len(yp) + 1)
        plt.plot(xp, yp, marker = "o")
        plt.show()