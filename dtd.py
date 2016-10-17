import Tkinter

oldx, oldy = 0, 0  # need to actually move cursor here - platform depedant


def motion(event):
    global oldx, oldy
    print event.x, event.y
    event.widget.create_line(oldx, oldy, event.x, event.y, smooth=True)
    oldx = event.x
    oldy = event.y


def main():
    top = Tkinter.Tk()
    frame = Tkinter.Canvas(top, bg="white", height=500, width=800)
    top.event_generate("<Motion>", warp=True, x=0, y=0)
    frame.bind("<Motion>", motion)
    frame.pack()
    top.mainloop()


if __name__ == "__main__":
    main()


from Tkinter import *

root = Tk()
