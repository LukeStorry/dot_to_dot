'''
DotToDot Program created for a Human-Computer-Interaction experiment.

A simple application to time drawing with different input devices.

Packaged in one long file for ease of distribution.

Written by Luke Storry with help from Ewam Stanley.

'''


import Tkinter
import time


# I hate globals but tkinter callback functions get messy without them.
precision, oldx, oldy, mb, canvas, input_type, diagram_type, start_time, dots_coords_lists, active_dots, drawn_dots = None, None, None, None, None, None, None, None, None, None, None


def set_global_vars():
    global precision, oldx, oldy, mb, canvas, input_type, diagram_type, start_time, dots_coords_lists, active_dots, drawn_dots
    precision = 5
    oldx, oldy = None, None
    mb = "up"
    canvas = None
    input_type = None
    diagram_type = None
    start_time = None

    vertices = [(100, 50), (180, 50), (280, 50), (400, 50), (470, 50), (470, 120), (470, 240), (470, 360), (310, 370), (100, 370), (100, 240), (100, 140), (100, 60), (
        170, 100), (280, 100), (420, 90), (380, 180), (320, 270), (270, 330), (200, 330), (270, 240), (340, 150), (270, 150), (180, 150), (160, 110)]
    dots_coords_lists = [[], []]
    for (x, y) in vertices:
        dots_coords_lists[0] += [(x, y)]
        dots_coords_lists[1] += [(y, x)]
    # assert len(dots_coords_lists[0]) == len(dots_coords_lists[1])
    active_dots = [False] * len(dots_coords_lists[0])
    drawn_dots = [False] * len(dots_coords_lists[0])


def input_t():
    global input_type
    input_type = "track"


def input_m():
    global input_type
    input_type = "mouse"


def diagram_0():
    global diagram_type
    diagram_type = 0


def diagram_1():
    global diagram_type
    diagram_type = 1


def choose_input(root):
    global input_type
    Tkinter.Button(root, text='Trackpad', command=input_t).pack()
    Tkinter.Button(root, text='Mouse', command=input_m).pack()
    while input_type == None:
        root.update()
        root.update_idletasks()
        time.sleep(0.1)


def choose_diagram(root):
    global diagram_type
    Tkinter.Button(root, text="Diagram 0", command=diagram_0).pack()
    Tkinter.Button(root, text="Diagram 1", command=diagram_1).pack()
    while diagram_type == None:
        root.update()
        root.update_idletasks()
        time.sleep(0.1)


def draw_canvas(root):
    global canvas, input_type
    canvas = Tkinter.Canvas(root, bg="white", height=500, width=500)

    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)
    draw_dots()
    canvas.pack()


def draw_dots():
    global dots_coords_lists
    for (x, y) in dots_coords_lists[diagram_type]:
        draw_oval(x, y, "red")
    first = dots_coords_lists[diagram_type][0]
    draw_oval(first[0], first[1], "green")


def mouse_button_press(event):
    global mb
    mb = "down"


def reset_active_dots():
    global active_dots
    for i in active_dots:
        active_dots[i] = False


def mouse_button_release(event):
    global mb, oldx, oldy
    mb = "up"
    reset_active_dots()
    oldx, oldy = None, None


def motion(event):
    # commented bits can be used to export a list of dots to contruct a diagram
    # import math
    if mb == "down":
        global oldx, oldy, precision
        # (x, y) = (str(int(math.ceil(event.x / 10.0)) * 10), str(int(math.ceil(event.y / 10.0)) * 10))
        # print x, y
        # with open("dotslist.txt", "a") as myfile:
        # myfile.write("(" + x + "," + y + "), ")
        if oldx is not None and oldy is not None:
            event.widget.create_line(
                oldx, oldy, event.x, event.y, width=precision * 2, capstyle=Tkinter.ROUND)
        hit_pixel(event.x, event.y)
        oldx, oldy = event.x, event.y
        # time.sleep(0.5)


def draw_oval(x, y, fill):
    global precision, canvas
    canvas.create_oval(x - precision, y - precision, x + precision, y + precision, fill=fill)


def hit_pixel(x, y):
    global drawn_dots, active_dots, precision, dots_coords_lists, diagram_type
    for dot_coords in dots_coords_lists[diagram_type]:
        if abs(dot_coords[0] - x) + abs(dot_coords[1] - y) < precision * 2:
            index = dots_coords_lists[diagram_type].index(dot_coords)

            # skip if already passed over
            if drawn_dots[index] and drawn_dots[index + 1]:
                return ''

            if index == 0:
                start_timer()

            # activate dot if previous is already drawn
            if drawn_dots[index - 1] or index == 0:
                active_dots[index] = True

            # draw dot if previous active & drawn
            if (drawn_dots[index - 1] and active_dots[index - 1]) or index == 0:
                draw_oval(dot_coords[0], dot_coords[1], "grey")
                drawn_dots[index] = True
                # if not last, colour next dot green
                if index != len(dots_coords_lists[diagram_type]) - 1:
                    next_dot_coords = dots_coords_lists[diagram_type][index + 1]
                    draw_oval(next_dot_coords[0], next_dot_coords[1], "green")


def all_drawn():
    global drawn_dots
    for drawn in drawn_dots:
        if not drawn:
            return False
    return True


def clear(root):
    for w in root.winfo_children():
        w.destroy()


def start_timer():
    global start_time
    if start_time == None:
        print ("Timer started.")
        start_time = time.clock()


def calculate_time_taken():
    global start_time
    print ("Timer ended.")
    return time.clock() - start_time


def calculate_result():
    return (time.strftime('%X %x %Z'), input_type, diagram_type, calculate_time_taken())


def append_to_csv(info, filename):
    with open(filename, "a") as myfile:
        for var in info:
            myfile.write(str(var) + ",")
        myfile.write("\n")


def main():
    append_to_csv(("Time", "Input Type", "Diagram Type", "Time Taken"), "results.csv")
    
    while True:
        set_global_vars()
        root = Tkinter.Tk()

        choose_input(root)
        clear(root)
        choose_diagram(root)
        clear(root)

        draw_canvas(root)
        while not all_drawn():
            root.update()
            root.update_idletasks()

        result = calculate_result()
        print result
        append_to_csv(result, "results.csv")
        clear(root)
        root.destroy()

if __name__ == "__main__":
    main()
