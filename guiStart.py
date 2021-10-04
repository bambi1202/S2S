import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import guiMain as Main

import os

command = ""
first_img_name = ""
second_img_name = ""

def push_button1():
    file_path = filedialog.askopenfilename(initialdir="genga")
    global first,first_img_name
    first_img = Image.open(file_path)
    w = first_img.width
    h = first_img.height
    first_img = first_img.resize((canvas_width,int(h * canvas_width/w)))
    first = ImageTk.PhotoImage(first_img)
    canvas.itemconfig(first_img_on_canvas,image=first,anchor=tk.NW, tags="first")
    first_img_name = os.path.basename(file_path).replace(".png", "")
    print(first_img_name)

def push_button2():
    file_path = filedialog.askopenfilename(initialdir="genga")
    global second,second_img_name
    second_img = Image.open(file_path)
    w = second_img.width
    h = second_img.height
    second_img = second_img.resize((canvas_width,int(h * canvas_width/w)))
    second = ImageTk.PhotoImage(second_img)
    canvas.itemconfig(second_img_on_canvas,image=second,anchor=tk.NW, tags="second")
    second_img_name = os.path.basename(file_path).replace(".png", "")
    print(second_img_name)

def push_button3():
    root.destroy()
    #cp = subprocess.run(["python 0604gui.py %s %s"%(first_img_name,second_img_name)])
    #cp = subprocess.run(["python /Users/ryoma/Desktop/workspace/GUItest/0604gui.py ex12 ex13"])
    Main.main(first_img_name,second_img_name)

root = tk.Tk()
root.title("First")
root.minsize(1070,540)
canvas_width = 390
canvas_higth = 540

canvas = tk.Canvas(bg="white", width=(canvas_width*2)+10, height=canvas_higth)
canvas.place(x=140, y=0)

first_img = Image.open("genga/first.png")
w = first_img.width
h = first_img.height
first_img = first_img.resize((canvas_width,int(h * canvas_width/w)))
first = ImageTk.PhotoImage(first_img)
first_img_on_canvas = canvas.create_image(0, 20, image=first, anchor=tk.NW, tags="first")

second_img = Image.open("genga/second.png")
w = second_img.width
h = second_img.height
second_img = second_img.resize((canvas_width,int(h * canvas_width/w)))
second = ImageTk.PhotoImage(second_img)
second_img_on_canvas = canvas.create_image((canvas_width)+10, 20, image=second, anchor=tk.NW, tags="second")

space = 50

Button1 = tk.Button(text='Frame\nStart',command=push_button1,height = 2, width = 8)
Button1.place(x = 10, y = 10)

Button2 = tk.Button(text='Frame\nEnd',command=push_button2,height = 2, width = 8)
Button2.place(x = 10, y = 10 +space*1)

Button3 = tk.Button(text='Start',command=push_button3,height = 2, width = 8)
Button3.place(x = 10, y = 10 +space*2)

root.mainloop()
