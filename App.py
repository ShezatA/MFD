from tkinter import *
import Pushup as p
import Squat as s

def pButton():
    top.destroy()
    p.main()

    main()

def sButton():
    top.destroy()
    s.main()

    main()

def main():
    global top
    top = Tk()
    top.eval('tk::PlaceWindow . center')
    top.title("WorkoutCV")
    top.iconbitmap("Muscle.ico")
    top.geometry("245x52")

    pBut = Button(top, text = "Pushup Detector", command=pButton, padx=15, pady=15)
    pBut.grid(column=0, row=1)
    sBut = Button(top, text = "Squat Detector ", command=sButton, padx=15, pady=15)
    sBut.grid(column=1, row=1)

    top.mainloop()

main()