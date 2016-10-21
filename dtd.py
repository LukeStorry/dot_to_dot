import Tkinter

precision = 5
oldx, oldy = None, None
mb = "up"
list_of_dots = {(50, 50): False, (100, 100): False,
                (100, 50): False, (50, 100): False, }


def choose_input():
    pass  # TODO


def draw_dots(canvas):
    global list_of_dots, precision
    for (x, y) in list_of_dots:
        canvas.create_oval(x - precision, y - precision, x + precision,
                           y + precision, fill="red")
    pass  # TODO


def initialise_canvas():
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, bg="white", height=800, width=1000)
    # TODO: maybe need to re-draw to make exp more streamlined
    draw_dots(canvas)
    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)
    canvas.pack()
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
        global oldx, oldy, precision
        # print (event.x, event.y)
        if oldx is not None and oldy is not None:
            event.widget.create_line(
                oldx, oldy, event.x, event.y, width=precision * 2, capstyle=Tkinter.ROUND)  # smooth = True)
        hit_pixel(event. x, event.y)
        oldx, oldy = event.x, event.y


def hit_pixel(x, y):
    global list_of_dots, precision
    print x, y
    for (i, j) in [(i, j) for i in range(x - precision, x + precision) for j in range(y - precision, y + precision)]:
        #print (i, j),
        if (i, j) in list_of_dots:
            print i, j, " hit"

    pass  # TODO: add to hitlist?


def main():
    initialise_canvas()
    choose_input()
    initalise_dots()

if __name__ == "__main__":
    main()
