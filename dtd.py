import Tkinter
import time

precision = 5
oldx, oldy = None, None
mb = "up"
canvas = None
# No longer used
dict_of_dots = None
#-
input_type = None
diagram_type = None
start_time = None
dots_coords_lists = [[(50, 50), (100, 100), (100, 50), (50, 100)],  # TODO populate with diagram vertices
                     [(150, 50), (100, 100), (100, 50), (50, 100)]]

assert len(dots_coords_lists[0]) == len(dots_coords_lists[1])
active_dots = [False] * len(dots_coords_lists[0])
drawn_dots = [False] * len(dots_coords_lists[0])


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
    if mb == "down":
        global oldx, oldy, precision
        #print (event.x, event.y)
        if oldx is not None and oldy is not None:
            event.widget.create_line(
                oldx, oldy, event.x, event.y, width=precision * 2, capstyle=Tkinter.ROUND)  # smooth = True)
        hit_pixel(event.x, event.y)
        oldx, oldy = event.x, event.y


def hit_pixel(x, y):
    global drawn_dots, active_dots, precision
    if diagram_type == "diagram1":
        dots = dots_coords_lists[0]
    else:
        dots = dots_coords_lists[1]

    for dot in dots:
        if ((x < dot[0] + 2 * precision) and (x > dot[0] - 2 * precision)) and ((y < dot[1] + 2 * precision) and (y > dot[1] - 2 * precision)):
            index = dots.index(dot)
            if index == 0:
                active_dots[0] = True
                drawn_dots[0] = True
            elif drawn_dots[index - 1] and active_dots[index - 1]:
                active_dots[index] = True
                drawn_dots[index] = True
            elif index > 0 and drawn_dots[index - 1] == True:
                active_dots[index] = True


def update_dots_drawings():
    pass  # TODO move code here


def input_t():
    global input_type
    input_type = "track"


def input_m():
    global input_type
    input_type = "mouse"


def diagram_1():
    global diagram_type
    diagram_type = "diagram1"


def diagram_2():
    global diagram_type
    diagram_type = "diagram2"


def start_timer():
    global start_time
    print ("Timer started.")
    start_time = time.clock()


def raise_button(event):
    event.widget.config(relief=Tkinter.RAISED)


def choose_input(root):
    global input_type
    Tkinter.Button(root, text='Trackpad', command=input_t,
                   relief=Tkinter.FLAT).pack()
    Tkinter.Button(root, text='Mouse', command=input_m,
                   relief=Tkinter.FLAT).pack()
    while input_type == None:
        root.update()
        root.update_idletasks()
        time.sleep(0.1)
    root.quit()


def choose_diagram(root):
    global diagram_type, dict_of_dots, dots_coords_lists
    Tkinter.Button(root, text='Diagram 1', command=diagram_1,
                   relief=Tkinter.FLAT).pack()
    Tkinter.Button(root, text='Diagram 2', command=diagram_2,
                   relief=Tkinter.FLAT).pack()
    while diagram_type == None:
        root.update()
        root.update_idletasks()
        time.sleep(0.1)
    root.quit()


def draw_canvas(root):
    global canvas, input_type
    canvas = Tkinter.Canvas(root, bg="white", height=400, width=1000)

    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)
    draw_dots()
    canvas.pack()


def draw_dots():
    global drawn_dots, precision, canvas
    next_node = False
    dots = None
    if diagram_type == "diagram1":
        dots = dots_coords_lists[0]
    else:
        dots = dots_coords_lists[1]

    i = 0

    for (x, y) in dots:
        # turn finished dots blue
        if drawn_dots[i]:
            canvas.create_oval(x - precision, y - precision, x + precision,
                               y + precision, fill="blue")
        elif next_node == False:
            # Draw the pair that need to be connected as green
            canvas.create_oval(x - precision, y - precision, x + precision, y + precision, fill="green")
            canvas.create_oval(dots[i - 1][0] - precision, dots[i - 1][1] - precision, dots[i - 1]
                               [0] + precision, dots[i - 1][1] + precision, fill="green")
            next_node = True
        else:
            # unfinished dots draw as  red
            canvas.create_oval(x - precision, y - precision, x + precision,
                               y + precision, fill="red")
        i = i + 1


def draw_start_button(root):
    Tkinter.Button(root, text='Start Timer', command=start_timer).pack()
    while start_time == None:
        root.update()
        root.update_idletasks()


def all_drawn():
    global drawn_dots
    for dot in drawn_dots:
        if not dot:
            return False
    return True


def clear(root):
    for w in root.winfo_children():
        w.destroy()


def calculate_time_taken():
    global start_time
    return time.clock() - start_time


def calculate_result():
    return (input_type, diagram_type, calculate_time_taken())


def append_to_csv(info, filename):
    with open(filename, "a") as myfile:
        for var in info:
            myfile.write(str(var) + ",")
        myfile.write("\n")


def main():
    root = Tkinter.Tk()
    root.bind('<Button-1>', raise_button)
    choose_input(root)
    choose_diagram(root)
    draw_canvas(root)
    draw_start_button(root)
    while not all_drawn():
        root.update()
        root.update_idletasks()
        time.sleep(0.1)

    result = calculate_result()
    append_to_csv(result, "results.csv")
    clear(root)
    root.destroy()

if __name__ == "__main__":
    main()
