from tkinter import *
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import guiMain as Main

import os

command = ""
first_img_name = ""
second_img_name = ""

def push_button1():
    file_path = filedialog.askopenfilename(initialdir="genga_new")
    global first,first_img_name
    first_img = Image.open(file_path)
    w = first_img.width
    h = first_img.height
    first_img = first_img.resize((canvas_width,int(h * canvas_width/w)))
    first = ImageTk.PhotoImage(first_img)
    canvas.itemconfig(first_img_on_canvas,image=first,anchor=NW, tags="first")
    first_img_name = os.path.basename(file_path).replace(".png", "")
    print(first_img_name)

def push_button2():
    file_path = filedialog.askopenfilename(initialdir="genga_new")
    global second,second_img_name
    second_img = Image.open(file_path)
    w = second_img.width
    h = second_img.height
    second_img = second_img.resize((canvas_width,int(h * canvas_width/w)))
    second = ImageTk.PhotoImage(second_img)
    canvas.itemconfig(second_img_on_canvas,image=second,anchor=NW, tags="second")
    second_img_name = os.path.basename(file_path).replace(".png", "")
    print(second_img_name)
    root.destroy()
    Main.main(first_img_name,second_img_name)

# def push_button3():
#     root.destroy()
#     #cp = subprocess.run(["python 0604gui.py %s %s"%(first_img_name,second_img_name)])
#     #cp = subprocess.run(["python /Users/ryoma/Desktop/workspace/GUItest/0604gui.py ex12 ex13"])
#     Main.main(first_img_name,second_img_name)

root = Tk()
root.title("Skeleton2Stroke -- please select the frames")
root.minsize(512*2 + 10*4, 512 + 10*2 + 60)
canvas_width = 512
canvas_higth = 512

canvas = Canvas(bg="white", width=(canvas_width*2)+10, height=canvas_higth)
canvas.place(x=10, y=80)

first_img = Image.open("genga_new/ex1_first.png")
w = first_img.width
h = first_img.height
first_img = first_img.resize((canvas_width,int(h * canvas_width/w)))
first = ImageTk.PhotoImage(first_img)
first_img_on_canvas = canvas.create_image(0, 0, image=first, anchor=NW, tags="first")

second_img = Image.open("genga_new/ex1_second.png")
w = second_img.width
h = second_img.height
second_img = second_img.resize((canvas_width,int(h * canvas_width/w)))
second = ImageTk.PhotoImage(second_img)
second_img_on_canvas = canvas.create_image(canvas_width, 0, image=second, anchor=NW, tags="second")

# space = 80


# icon1 = PhotoImage(file='iconimg/startframe.png')
# Button1 = Button(image=icon1, command=push_button1)
# Button1.place(x = 10, y = 10, height = 60, width = 80)
# # Button1 = tk.Button(text='Frame\nStart',command=push_button1,height = 2, width = 8)
# # Button1 = tk.Button(image=icon1,command=push_button1).pack(anchor=tk.N,side=tk.LEFT)
# # Button1.place(x = 10, y = 10)

# icon2 = PhotoImage(file='iconimg/endframe.png')
# Button2 = Button(image=icon2, command=push_button2)
# Button2.place(x = 10 +space*1, y = 10, height = 60, width = 80)
# Button2 = tk.Button(text='Frame\nEnd',command=push_button2,height = 2, width = 8)
# Button2 = tk.Button(image=icon2,command=push_button2).pack(anchor=tk.N,side=tk.LEFT)
# Button2.place(x = 10, y = 10 +space*1)

# icon3 = tk.PhotoImage(file='iconimg/pen.png')
# Button3 = tk.Button(image=icon3, command=push_button3)
# Button3.place(x = 10 +space*2, y = 10, height = 60, width = 80)
# Button3 = tk.Button(text='Start',command=push_button3,height = 2, width = 8)
# Button3 = tk.Button(image=icon3,command=push_button3).pack(anchor=tk.N,side=tk.LEFT)
# Button3.place(x = 10, y = 10 +space*2)

def invalid_button_press():
    print('invalid')

space = 80


icon1 = PhotoImage(file='iconimg/rubber.png')
Button1 = Button(image=icon1, command=invalid_button_press)
Button1.place(x = 10, y = 10, height = 60, width = 80)

# icon2 = PhotoImage(file='iconimg/finishcorretion.png')
icon2 = PhotoImage(file='iconimg/savebutton.png')
Button2 = Button(image=icon2, command=invalid_button_press)
Button2.place(x = 10 +space*1, y = 10, height = 60, width = 80)

icon3 = PhotoImage(file='iconimg/startframe.png')
Button3 = Button(image=icon3, command=push_button1)
Button3.place(x = 10 +space*2, y = 10, height = 60, width = 80)

icon4 = PhotoImage(file='iconimg/endframe.png')
Button4 = Button(image=icon4, command=push_button2)
Button4.place(x = 10 +space*3, y = 10, height = 60, width = 80)

icon5 = PhotoImage(file='iconimg/poseestimation.png')
Button5 = Button(image=icon5, command=invalid_button_press)
Button5.place(x = 10 +space*4, y = 10, height = 60, width = 80)

icon6 = PhotoImage(file='iconimg/addskeleton.png')
Button6 = Button(image=icon6, command=invalid_button_press)
Button6.place(x = 10 +space*5, y = 10, height = 60, width = 80)

icon7 = PhotoImage(file='iconimg/applyskeleton.png')
Button7 = Button(image=icon7, command=invalid_button_press)
Button7.place(x = 10 +space*6, y = 10, height = 60, width = 80)

icon8 = PhotoImage(file='iconimg/skeletonoff.png')
Button8 = Button(image=icon8, command=invalid_button_press)
Button8.place(x = 10 +space*7, y = 10, height = 60, width = 80)

icon9 = PhotoImage(file='iconimg/applycorrection.png')
Button9 = Button(image=icon9, command=invalid_button_press)
Button9.place(x = 10 +space*8, y = 10, height = 60, width = 80)

icon10 = PhotoImage(file='iconimg/finishcorretion.png')
Button10 = Button(image=icon10, command=invalid_button_press)
Button10.place(x = 10 +space*9, y = 10, height = 60, width = 80)

root.mainloop()
