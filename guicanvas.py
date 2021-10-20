from tkinter import *
from PIL import ImageGrab, Image, ImageTk
import cv2
import numpy as np
import os

root = Tk()
root.title("Skeleton2Stroke -- please draw the draft")

canvas_width = 512
canvas_height = 512
edge = 10
root.minsize(canvas_width*2 + edge*4, canvas_height + edge*2+60)


first = Canvas(root, width=canvas_width+edge, height=canvas_height, background='white')
first.place(x=edge, y=edge+60)
second = Canvas(root, width=canvas_width+edge, height=canvas_height, background='white')
second.place(x=edge*2 + canvas_width, y=edge+60)


show_shadow = True
rubber_flag = False

x_list = []
y_list = []
rubber_x = []
rubber_y = []

pressed_tag = False

def pressed(event):
    global x_list, y_list, pressed_tag
    pressed_tag = True
    x1, y1 = event.x, event.y
    x_list.append(x1)
    y_list.append(y1)

def dragged_first(event):  
    global x_list, y_list, pressed_tag  
    x1, y1 = event.x, event.y
    x_list.append(x1)
    y_list.append(y1)

    print(rubber_flag)
    
    for i in range(len(x_list)):
        if i > 1:
            if rubber_flag == False:
                first.create_line(x_list[i],y_list[i],x_list[i-1],y_list[i-1],fill='black',width=5,tags='line')
                second.create_line(x_list[i],y_list[i],x_list[i-1],y_list[i-1],fill='gray',dash=(2,4),tags='line')
            else:
                first.create_line(x_list[i],y_list[i],x_list[i-1],y_list[i-1],fill='white',width=30,tags='line')
                second.create_line(x_list[i],y_list[i],x_list[i-1],y_list[i-1],fill='white',width=30,tags='line')

def dragged_second(event):
    global x_list, y_list, pressed_tag          
    x1, y1 = event.x, event.y
    x_list.append(x1)
    y_list.append(y1)

  
    if rubber_flag == False:
        for i in range(len(x_list)):
            if i > 1:
                second.create_line(x_list[i],y_list[i],x_list[i-1],y_list[i-1],fill='black',width=5,tags='line')
        
def released(event):
    global x_list, y_list, pressed_tag
    pressed_tag = False            
    x_list = []
    y_list = []
    
def rubber():
    global rubber_flag
    if rubber_flag:
        rubber_flag = False
    else:
        rubber_flag = True

def save_button():
    first_saver(first)
    second_saver(second)    
    root.destroy()
    os.system("python guiStart.py")

def first_saver(widget):
    widget.update()
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    xx=x+widget.winfo_width()
    yy=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,xx,yy)).save('genga_new/ex9_first.png')
    ImageGrab.grab().crop((x,y,xx,yy)).save('genga/ex9_first.png')

def second_saver(widget):
    widget.update()
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    xx=x+widget.winfo_width()
    yy=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,xx,yy)).save('test_second.png')
    image=cv2.imread('test_second.png',cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([0,0,0])
    high_hsv = np.array([180,255,46])
    gray_mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)
    cv2.imwrite('test_second_black.png',gray_mask)
    gray_img = cv2.imread('test_second_black.png')
    img_info = gray_img.shape
    h = img_info[0]
    w = img_info[1]
    gray = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
    dst = np.zeros((h,w,1), np.uint8)
    for i in range(h):
        for j in range(w):
            gray_pix = 255 - gray[i,j]
            dst[i,j] =gray_pix

    cv2.imwrite('genga_new/ex9_second.png',dst)
    cv2.imwrite('genga/ex9_second.png',dst)

#将画布与鼠标左键进行绑定
first.bind('<ButtonPress-1>', pressed) 
first.bind('<B1-Motion>', dragged_first)
first.bind('<ButtonRelease-1>', released)


second.bind('<ButtonPress-1>', pressed) 
second.bind('<B1-Motion>', dragged_second)
second.bind('<ButtonRelease-1>', released)


# Label(root, text='按住鼠标左键并移动，开始绘制').pack(side=BOTTOM)

def invalid_button_press():
    print('invalid')


space = 80

icon1 = PhotoImage(file='iconimg/rubber.png')
Button1 = Button(image=icon1, command=rubber)
Button1.place(x = 10, y = 10, height = 60, width = 80)

# icon2 = PhotoImage(file='iconimg/finishcorretion.png')
icon2 = PhotoImage(file='iconimg/savebutton.png')
Button2 = Button(image=icon2, command=save_button)
Button2.place(x = 10 +space*1, y = 10, height = 60, width = 80)

icon3 = PhotoImage(file='iconimg/startframe.png')
Button3 = Button(image=icon3, command=rubber)
Button3.place(x = 10 +space*2, y = 10, height = 60, width = 80)

icon4 = PhotoImage(file='iconimg/endframe.png')
Button4 = Button(image=icon4, command=rubber)
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