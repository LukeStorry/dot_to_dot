import Tkinter


oldx, oldy = 0, 0  # need to actually move cursor here - platform depedant
list_of_dots = []


def initalise_dots():
    pass  # TODO


def motion(event):
    global oldx, oldy, list_of_dots
    print event.x, event.y
    event.widget.create_line(oldx, oldy, event.x, event.y, smooth=True)
    oldx, oldy = event.x, event.y

    if (event.x, event.y) in list_of_dots:
        pass  # TODO


def main():
    top = Tkinter.Tk()
    frame = Tkinter.Canvas(top, bg="white", height=500, width=800)
    top.event_generate("<Motion>", warp=True, x=0, y=0)  # only works in linux
    frame.bind("<Motion>", motion)
    frame.pack()
    top.mainloop()


if __name__ == "__main__":
    main()
