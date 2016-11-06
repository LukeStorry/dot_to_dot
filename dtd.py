import Tkinter
import time

precision = 5
oldx, oldy = None, None
mb = "up"
canvas = None
#No longer used
dict_of_dots = None
#-
input_type = None
diagram_type = None
start_time = None
dots_lists = [[(50, 50), (100, 100), (100, 50), (50, 100)],
              [(150, 50), (100, 100), (100, 50), (50, 100)]]

#ADDED:
#Bool array: During the duration of a mouse press, any hit nodes are set to true.
#When the mouse press is lifted, the whole array is set to False again.
#Only valid if the nodes are hit consecutively in the order of the array.
active_dots = [False] * len(dots_lists[0])

#Dots that have been connected
drawn_dots = [False] * len(dots_lists[0])

#Red = undrawn
#Green = Pair to be drawn
#Blue = drawn


def mouse_button_press(event):
    global mb
    mb = "down"

#Added
def reset_active_dots():
    global active_dots
    for i in active_dots:
        active_dots[i] = False

#Changed
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

#Changed
def hit_pixel(x, y):
    global drawn_dots, active_dots, precision

    ''' Old code
    # print x, y
    for (i, j) in [(i, j) for i in range(x - 2 * precision, x + 2 * precision) for j in range(y - 2 * precision, y + 2 * precision)]:
        # print (i, j),
        if (i, j) in dict_of_dots:
            # print i, j, " hit"          
            index = dict_of_dots.index((i,j))
            if index > 0 and dict_of_dots[index - 1] == True and active_dots[index - 1] == True:
                active_dots[index] = True
                dict_of_dots[index] = True
            elif index == 0:
                active_dots[0] = True'''

    dots = None

    if diagram_type == "diagram1":
        dots = dots_lists[0]
    else:
        dots = dots_lists[1]

    for dot in dots:
        if ((x < dot[0] + 2*precision) and (x > dot[0] - 2*precision)) and ((y < dot[1] + 2*precision) and (y > dot[1] - 2*precision)):
            index = dots.index(dot)
            if index > 0 and drawn_dots[index - 1] == True and active_dots[index - 1] == True:
                active_dots[index] = True
                drawn_dots[index] = True
            elif index > 0 and drawn_dots[index - 1] == True:
                active_dots[index] = True
            elif index == 0:
                active_dots[0] = True
                drawn_dots[0] = True
            draw_dots()

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

#Changed
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
    dict_of_dots[0] = True

##Changed
def draw_canvas(root):
    global canvas, input_type
    canvas = Tkinter.Canvas(root, bg="white", height=400, width=1000)

    canvas.bind("<Motion>", motion)
    canvas.bind("<ButtonPress-1>", mouse_button_press)
    canvas.bind("<ButtonRelease-1>", mouse_button_release)

    draw_dots()
    
    canvas.pack()

##Changed
def draw_dots():
    # draw dots
    global drawn_dots, precision, canvas
    next_node = False

    dots = None

    if diagram_type == "diagram1":
        dots = dots_lists[0]
    else:
        dots = dots_lists[1]

    i = 0

    for dot in dots:
        x = dot[0]
        y = dot[1]
        if drawn_dots[i] == True:
            canvas.create_oval(x - precision, y - precision, x + precision,
                           y + precision, fill="blue")
        elif next_node == False:
            #Draw the pair that need to be connected as green
            canvas.create_oval(x - precision, y - precision, x + precision,
                           y + precision, fill="green")
            canvas.create_oval(dots[i-1][0] - precision, dots[i-1][1] - precision, dots[i-1][0] + precision,
                           dots[i-1][1] + precision, fill="green")
            next_node = True
        else:
            canvas.create_oval(x - precision, y - precision, x + precision,
                               y + precision, fill="red")
        i = i + 1

def draw_start_button(root):
    Tkinter.Button(root, text='Start Timer', command=start_timer).pack()
    while start_time == None:
        root.update()
        root.update_idletasks()


##Changed
def all_hit():
    global drawn_dots
    for dot in drawn_dots:
        if dot == False:
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
    while not all_hit():
        root.update()
        root.update_idletasks()
        time.sleep(0.1)

    result = calculate_result()
    append_to_csv(result, "results.csv")
    #Changed
    clear(root)
    root.destroy()

if __name__ == "__main__":
    main()
