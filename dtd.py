import Tkinter
import time

precision = 5
oldx, oldy = None, None
mb = "up"
canvas = None
dict_of_dots = None
input_type = None
diagram_type = None
start_time = None
dots_lists = [[(50, 50), (100, 100), (100, 50), (50, 100)],
              [(150, 50), (100, 100), (100, 50), (50, 100)]]


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
        #print (event.x, event.y)
        if oldx is not None and oldy is not None:
            event.widget.create_line(
                oldx, oldy, event.x, event.y, width=precision * 2, capstyle=Tkinter.ROUND)  # smooth = True)
        hit_pixel(event.x, event.y)
        oldx, oldy = event.x, event.y


def hit_pixel(x, y):
    global dict_of_dots, precision, canvas
    print x, y
    for (i, j) in [(i, j) for i in range(x - precision, x + precision) for j in range(y - precision, y + precision)]:
        # print (i, j),
        if (i, j) in dict_of_dots:
            print i, j, " hit"
            canvas.create_oval(i - precision, j - precision,
                               i + precision, j + precision, fill="red")

            dict_of_dots[(i, j)] = True


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
    global diagram_type, dict_of_dots, dots_lists
    Tkinter.Button(root, text='Diagram 1', command=diagram_1,
                   relief=Tkinter.FLAT).pack()
    Tkinter.Button(root, text='Diagram 2', command=diagram_2,
                   relief=Tkinter.FLAT).pack()
    while diagram_type == None:
        root.update()
        root.update_idletasks()
        time.sleep(0.1)
    root.quit()
    if diagram_type == "diagram1":
        dots = dots_lists[0]
    else:
        dots = dots_lists[1]
    dict_of_dots = {}
    for dot in dots:
        dict_of_dots[dot] = False


def draw_canvas(root):
    global dict_of_dots, canvas, input_type
    canvas = Tkinter.Canvas(root, bg="white", height=400, width=1000)

    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)

    # draw dots
    for (x, y) in dict_of_dots:
        canvas.create_oval(x - precision, y - precision, x + precision,
                           y + precision, fill="blue")
    canvas.pack()


def draw_start_button(root):
    Tkinter.Button(root, text='Start Timer', command=start_timer).pack()
    while start_time == None:
        root.update()
        root.update_idletasks()


def all_hit():
    global dict_of_dots
    for dot in dict_of_dots:
        if dict_of_dots[dot] == False:
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


def write_result(result):
    with open("results.csv", "a") as myfile:
        myfile.write(str(result))


def main():
    root = Tkinter.Tk()
    root.bind('<Button-1>', raise_button)
    choose_input(root)
    choose_diagram(root)
    draw_canvas(root)
    draw_start_button(root)
    while not all_hit():
        root.update()
        root.update_idletasks()
        time.sleep(0.1)

    result = calculate_result()
    print result
    write_result(result)

if __name__ == "__main__":
    main()
