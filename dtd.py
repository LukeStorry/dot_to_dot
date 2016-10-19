import Tkinter


def choose_input(root):
    pass  # TODO


def initalise_dots(root):
    pass  # TODO


oldx, oldy = None, None
mb = "up"


def initialise_canvas():
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, bg="white", height=800, width=1000)
    canvas.pack()
    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)
    root.mainloop()


def mouse_button_press(event):
    global mb
    mb = "down"


def mouse_button_release(event):
    global mb, oldx, oldy
    mb = "up"
    oldx, oldy = None, None


def motion(event):
    if mb == "down":
        global oldx, oldy
        if oldx is not None and oldy is not None:
            event.widget.create_line(oldx, oldy, event.x, event.y, smooth=True)
        oldx, oldy = event.x, event.y


def main():
    initialise_canvas()
    choose_input()
    initalise_dots()

if __name__ == "__main__":
    main()
