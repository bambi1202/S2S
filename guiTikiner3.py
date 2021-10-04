import cv2
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import numpy as np
import random

import csv
import pprint


import guiImg as Img
import guiDict as Dict
import guiGreed as Greed

info_dict = {}
UIseedlist = [0,0]
add_linelist = []
add_first_line_list = []
add_second_line_list = []

canvas = 0
addtime = 0
B5flag = True
parts_list = []

def pressed(event):
	global pressed_x, pressed_y, tag
	item_id = canvas.find_closest(event.x, event.y)
	tag = canvas.gettags(item_id[0])[0]
	print(tag)
	pressed_x = event.x
	pressed_y = event.y

def dragged(event):
	global pressed_x, pressed_y, tag
	delta_x = event.x - pressed_x
	delta_y = event.y - pressed_y
	x0, y0, x1, y1 = canvas.coords(tag)
	canvas.coords(tag, x0+delta_x, y0+delta_y, x1+delta_x, y1+delta_y)
	pressed_x = event.x
	pressed_y = event.y
	draw_line()

def draw_line():
	line_list = [["first_head","first_neck"],["first_head","first_r_eye"],["first_head","first_l_eye"],["first_r_ear","first_r_eye"],["first_l_ear","first_l_eye"],["first_neck","first_r_shoulder"],["first_neck","first_l_shoulder"],["first_r_elbow","first_r_shoulder"],["first_l_elbow","first_l_shoulder"],
	["first_r_elbow","first_r_hand"],["first_l_elbow","first_l_hand"],
	["first_neck","first_r_leg"],["first_neck","first_l_leg"],["first_r_knee","first_r_leg"],["first_l_knee","first_l_leg"],["first_r_knee","first_r_foot"],["first_l_knee","first_l_foot"],
	["second_head","second_neck"],["second_head","second_r_eye"],["second_head","second_l_eye"],["second_r_ear","second_r_eye"],["second_l_ear","second_l_eye"],["second_neck","second_r_shoulder"],["second_neck","second_l_shoulder"],["second_r_elbow","second_r_shoulder"],["second_l_elbow","second_l_shoulder"],
	["second_r_elbow","second_r_hand"],["second_l_elbow","second_l_hand"],
	["second_neck","second_r_leg"],["second_neck","second_l_leg"],["second_r_knee","second_r_leg"],["second_l_knee","second_l_leg"],["second_r_knee","second_r_foot"],["second_l_knee","second_l_foot"]
	]
	canvas.delete("line")
	for line in line_list:
		tag1 = line[0]
		tag2 = line[1]
		x01, y01, x11, y11 = canvas.coords(tag1)
		x02, y02, x12, y12 = canvas.coords(tag2)
		canvas.create_line((x01+x11)/2,(y01+y11)/2,(x02+x12)/2,(y02+y12)/2,fill="red",tags="line")

	if len(add_linelist)>0:
		for add_line in add_linelist:
			add_tag1 = add_line[0]
			add_tag2 = add_line[1]
			x01, y01, x11, y11 = canvas.coords(add_tag1)
			x02, y02, x12, y12 = canvas.coords(add_tag2)
			canvas.create_line((x01+x11)/2,(y01+y11)/2,(x02+x12)/2,(y02+y12)/2,fill="blue",tags="line")


def first_pressed(event):
	global pressed_x, pressed_y, tag, base_dict,canvas,UIseedlist
	first_img_label = info_dict["first_img_label"]
	first_img_name = info_dict["first_img_name"]

	item_id = canvas.find_closest(event.x, event.y)
	tag = canvas.gettags(item_id[0])[0]
	print(tag)
	pressed_x = event.x
	pressed_y = event.y
	print((first_img_label[int(pressed_y),int(pressed_x)]))
	UIseedlist[0] = (first_img_label[int(pressed_y),int(pressed_x)])
	txt1.delete(0,tk.END)
	txt1.insert(tk.END,(first_img_label[int(pressed_y),int(pressed_x)]))
	txt3.delete(0,tk.END)
	txt3.insert(tk.END,(base_dict[first_img_name]["label"+str(first_img_label[int(pressed_y),int(pressed_x)])]["pair"]).replace('label',''))

def second_pressed(event):
	global pressed_x, pressed_y, tag, all_dict,canvas,UIseedlist
	second_img_label = info_dict["second_img_label"]
	second_img_name = info_dict["second_img_name"]
	width = info_dict["width"]
	canvas_width = width

	item_id = canvas.find_closest(event.x, event.y)
	tag = canvas.gettags(item_id[0])[0]
	print(tag)
	pressed_x = event.x
	pressed_y = event.y
	print((second_img_label[int(pressed_y),int(pressed_x-((canvas_width)+10))]))
	UIseedlist[1] = (second_img_label[int(pressed_y),int(pressed_x-((canvas_width)+10))])
	txt2.delete(0,tk.END)
	txt2.insert(tk.END,(second_img_label[int(pressed_y),int(pressed_x-((canvas_width)+10))]))
	txt4.delete(0,tk.END)
	txt4.insert(tk.END,(base_dict[second_img_name]["label"+str(second_img_label[int(pressed_y),int(pressed_x-((canvas_width)+10))])]["pair"]).replace('label',''))

def detail_correction():
	first_img_label = info_dict["first_img_label"]
	first_img_name = info_dict["first_img_name"]
	second_img_label = info_dict["second_img_label"]
	second_img_name = info_dict["second_img_name"]
	height = info_dict["height"]
	width = info_dict["width"]

	status.delete("1.0","end")
	status.insert(tk.END,("detail_correction\nbusy"))

	global modi_first_img,modi_second_img

	seedlist = ("label" + str(UIseedlist[0]),"label" + str(UIseedlist[1]))
	print(seedlist)
	Dict.add_score(10000,base_dict,first_img_name,second_img_name,seedlist[0],seedlist[1])

	Greed.greed(info_dict["greed_weight"],base_dict,first_img_name,second_img_name)

	first_result_img,second_result_img = Img.make_result_img(height,width,base_dict,first_img_name,second_img_name,first_img_label,second_img_label)

	modi_first_img = convert(first_result_img)
	modi_second_img = convert(second_result_img)
	canvas.itemconfig(first_img_on_canvas,image=modi_first_img,anchor=tk.NW, tags="first")
	canvas.itemconfig(second_img_on_canvas,image=modi_second_img,anchor=tk.NW, tags="second")

	status.delete("1.0","end")
	status.insert(tk.END,("detail_correction\ndone"))

def apply_skelton_Information():
	status.delete("1.0","end")
	status.insert(tk.END,("apply_skelton\nbusy"))
	global modi_first_img,modi_second_img
	div = 50
	r = 2

	bone_dict = {}
	first_bone_dict = {}
	second_bone_dict = {}
	score_dict = {}
	first_score_dict = {}
	second_score_dict = {}

	first_img_label = info_dict["first_img_label"]
	first_img_name = info_dict["first_img_name"]
	second_img_label = info_dict["second_img_label"]
	second_img_name = info_dict["second_img_name"]
	height = info_dict["height"]
	width = info_dict["width"]
	canvas_width = width
	canvas_height = height
	first_img_linelabel = info_dict["first_img_linelabel"]
	first_img_BGlabel = info_dict["first_img_BGlabel"]
	second_img_linelabel = info_dict["second_img_linelabel"]
	second_img_BGlabel = info_dict["second_img_BGlabel"]

	first_line_list = [["first_head","first_neck"],["first_head","first_r_eye"],["first_head","first_l_eye"],["first_r_ear","first_r_eye"],["first_l_ear","first_l_eye"],["first_neck","first_r_shoulder"],["first_neck","first_l_shoulder"],["first_r_elbow","first_r_shoulder"],["first_l_elbow","first_l_shoulder"],
	["first_r_elbow","first_r_hand"],["first_l_elbow","first_l_hand"],
	["first_neck","first_r_leg"],["first_neck","first_l_leg"],["first_r_knee","first_r_leg"],["first_l_knee","first_l_leg"],["first_r_knee","first_r_foot"],["first_l_knee","first_l_foot"]]

	second_line_list = [["second_head","second_neck"],["second_head","second_r_eye"],["second_head","second_l_eye"],["second_r_ear","second_r_eye"],["second_l_ear","second_l_eye"],["second_neck","second_r_shoulder"],["second_neck","second_l_shoulder"],["second_r_elbow","second_r_shoulder"],["second_l_elbow","second_l_shoulder"],
	["second_r_elbow","second_r_hand"],["second_l_elbow","second_l_hand"],
	["second_neck","second_r_leg"],["second_neck","second_l_leg"],["second_r_knee","second_r_leg"],["second_l_knee","second_l_leg"],["second_r_knee","second_r_foot"],["second_l_knee","second_l_foot"]]

	if len(add_first_line_list) >0:
		first_line_list.extend(add_first_line_list)
	if len(add_second_line_list) >0:
		second_line_list.extend(add_second_line_list)

	for line in first_line_list:
		linelabel = 0
		bglabel = 1
		tag1 = line[0]
		tag2 = line[1]
		x01, y01, x11, y11 = canvas.coords(tag1)
		x02, y02, x12, y12 = canvas.coords(tag2)
		crossed_area_list = []
		pre_label = -1
		line_name = tag1 +"/"+ tag2
		for i in range(div):
			label = (first_img_label[int((y02+y12)/2+(((y01+y11)/2 - (y02+y12)/2)*i/div)),int((x02+x12)/2+(((x01+x11)/2 - (x02+x12)/2)*i/div))])
			crossed_area_list.append(label)
		first_bone_dict[line_name] = crossed_area_list

	bone_dict[first_img_name] = first_bone_dict

	for line in second_line_list:
		linelabel = 0
		bglabel = 1
		tag1 = line[0]
		tag2 = line[1]
		x01, y01, x11, y11 = canvas.coords(tag1)
		x02, y02, x12, y12 = canvas.coords(tag2)
		crossed_area_list = []
		pre_label = -1
		line_name = tag1 +"/"+ tag2
		for i in range(div):
			label = (second_img_label[int((y02+y12)/2+(((y01+y11)/2 - (y02+y12)/2)*i/div)),int((x02+x12)/2+(((x01+x11)/2 - (x02+x12)/2)*i/div)-((canvas_width)+10))])
			crossed_area_list.append(label)
		second_bone_dict[line_name] = crossed_area_list

	bone_dict[second_img_name] = second_bone_dict

	for i in  range(len(first_line_list)):
		for j in range(r,div-r):
			n = (bone_dict[first_img_name][first_line_list[i][0] +"/"+ first_line_list[i][1]][j])
			#m = (bone_dict[second_img_name][second_line_list[i][0] +"/"+ second_line_list[i][1]][j])
			for k in range(2*r):
				m = (bone_dict[second_img_name][second_line_list[i][0] +"/"+ second_line_list[i][1]][j-r+k])
				if n != first_img_linelabel and n != first_img_BGlabel and m != second_img_linelabel and m != second_img_BGlabel:
					Dict.add_score(30,base_dict,first_img_name,second_img_name,"label"+str(n),"label"+str(m))



	Dict.set_pair(base_dict,first_img_name,second_img_name)

	first_result_img,second_result_img = Img.make_result_img(height,width,base_dict,first_img_name,second_img_name,first_img_label,second_img_label)

	modi_first_img = convert(first_result_img)
	modi_second_img = convert(second_result_img)
	canvas.itemconfig(first_img_on_canvas,image=modi_first_img,anchor=tk.NW, tags="first")
	canvas.itemconfig(second_img_on_canvas,image=modi_second_img,anchor=tk.NW, tags="second")

	status.delete("1.0","end")
	status.insert(tk.END,("apply_skelton\ndone"))

def add_skelton():
	global addtime
	r = 7

	img_width = info_dict["img_width"]
	img_height = info_dict["img_height"]
	height = info_dict["height"]
	width = info_dict["width"]
	canvas_width = width
	canvas_height = height

	color1 = np.array(random.randint(100000,499999))
	color2 = np.array(random.randint(500000,999999))

	print("add")
	addtime += 1
	add_linelist.append(["first_1add"+str(addtime),"first_2add"+str(addtime)])
	add_first_line_list.append(["first_1add"+str(addtime),"first_2add"+str(addtime)])
	canvas.create_oval(100*img_width/300-r,100*img_height/500-r,100*img_width/300+r,100*img_height/500+r, fill="#"+str(color1), tags="first_1add"+str(addtime))
	canvas.create_oval(120*img_width/300-r,100*img_height/500-r,120*img_width/300+r,100*img_height/500+r, fill="#"+str(color2), tags="first_2add"+str(addtime))
	canvas.tag_bind("first_1add"+str(addtime), "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_2add"+str(addtime), "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_1add"+str(addtime), "<B1-Motion>", dragged)
	canvas.tag_bind("first_2add"+str(addtime), "<B1-Motion>", dragged)

	add_linelist.append(["second_1add"+str(addtime),"second_2add"+str(addtime)])
	add_second_line_list.append(["second_1add"+str(addtime),"second_2add"+str(addtime)])
	canvas.create_oval((canvas_width+10)+100*img_width/300-r,100*img_height/500-r,(canvas_width+10)+100*img_width/300+r,100*img_height/500+r, fill="#"+str(color1), tags="second_1add"+str(addtime))
	canvas.create_oval((canvas_width+10)+120*img_width/300-r,100*img_height/500-r,(canvas_width+10)+120*img_width/300+r,100*img_height/500+r, fill="#"+str(color2), tags="second_2add"+str(addtime))
	canvas.tag_bind("second_1add"+str(addtime), "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_2add"+str(addtime), "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_1add"+str(addtime), "<B1-Motion>", dragged)
	canvas.tag_bind("second_2add"+str(addtime), "<B1-Motion>", dragged)

def hide_skelton():
    global B5flag,parts_list,canvas
    print(B5flag)
    if (B5flag == True):
        for parts in parts_list:
            canvas.lower("first_"+parts[0])
            canvas.lower("second_"+parts[0])
            canvas.lower("line")
            B5text.set("Skeleton\nON")
            B5flag = False
    else:
        for parts in parts_list:
            canvas.lift("first_"+parts[0])
            canvas.lift("second_"+parts[0])
            canvas.lift("line")
            B5text.set("Skeleton\nOFF")
            B5flag = True
	#canvas.delete("first")


def finish_correction():
	first_img_label = info_dict["first_img_label"]
	first_img_name = info_dict["first_img_name"]
	second_img_label = info_dict["second_img_label"]
	second_img_name = info_dict["second_img_name"]

	status.delete("1.0","end")
	status.insert(tk.END,("finish_correction\nbusy"))
	global result_first_img,result_second_img

	first_line_list = Img.make_linelist(info_dict["height"],info_dict["width"],info_dict["first_img_label"],info_dict["first_img_n"],info_dict["first_divied_line_img_n"],info_dict["first_divied_line_img_label"],info_dict["first_skeleton"],info_dict["first_img_linelabel"])
	second_line_list = Img.make_linelist(info_dict["height"],info_dict["width"],info_dict["second_img_label"],info_dict["second_img_n"],info_dict["second_divied_line_img_n"],info_dict["second_divied_line_img_label"],info_dict["second_skeleton"],info_dict["second_img_linelabel"])

	base_dict[first_img_name]["label"+str(info_dict["first_img_BGlabel"])]["pair"] = "label"+str(info_dict["second_img_BGlabel"])
	base_dict[second_img_name]["label"+str(info_dict["second_img_BGlabel"])]["pair"] = "label"+str(info_dict["first_img_BGlabel"])
	base_dict[first_img_name]["label"+str(info_dict["first_img_linelabel"])]["pair"] = "label"+str(info_dict["second_img_linelabel"])
	base_dict[second_img_name]["label"+str(info_dict["second_img_linelabel"])]["pair"] = "label"+str(info_dict["first_img_linelabel"])

	for i in first_line_list:
		i[0] = int(base_dict[first_img_name]["label"+str(i[0])]["pair"].replace('label',''))
		i[1] = int(base_dict[first_img_name]["label"+str(i[1])]["pair"].replace('label',''))

	colorlist = np.zeros((info_dict["first_divied_line_img_n"],info_dict["second_divied_line_img_n"],3), np.uint8)
	print(colorlist)
	result_second_img = Img.coloring_line(info_dict["height"],info_dict["width"],info_dict["second_junction_list"],colorlist,second_line_list,info_dict["second_divied_line_img_label"],info_dict["second_divied_line_img_data"],info_dict["second_img_label"],info_dict["second_img_BGlabel"],info_dict["second_img_linelabel"])
	result_first_img = Img.coloring_line(info_dict["height"],info_dict["width"],info_dict["first_junction_list"],colorlist,first_line_list,info_dict["first_divied_line_img_label"],info_dict["first_divied_line_img_data"],info_dict["first_img_label"],info_dict["first_img_BGlabel"],info_dict["first_img_linelabel"])

	#result,result_first_img,result_second_img = makematchimg(first_img_name,second_img_name,first_img,second_img,first_img_n,second_img_n,5,2,3,True)
	result_first_img = convert(result_first_img)
	result_second_img = convert(result_second_img)
	canvas.itemconfig(first_img_on_canvas,image=result_first_img,anchor=tk.NW, tags="first")
	canvas.itemconfig(second_img_on_canvas,image=result_second_img,anchor=tk.NW, tags="second")
	status.delete("1.0","end")
	status.insert(tk.END,("finish_correction\ndone"))

def select_firstImg():
	img_width = info_dict["img_width"]
	img_height = info_dict["img_height"]
	print("select_firstImg")
	parts_list = [["head",100,100,"red"],["r_eye",110,100,"red"],["l_eye",90,100,"red"],["r_ear",130,100,"red"],["l_ear",70,100,"red"],["neck",100,200,"red"],
	["r_shoulder",150,200,"blue"],["l_shoulder",50,200,"green"],["r_elbow",170,230,"blue"],["l_elbow",30,230,"green"],["r_hand",170,260,"blue"],["l_hand",30,260,"green"],
	["r_leg",150,300,"yellow"],["l_leg",50,300,"pink"],["r_knee",150,400,"yellow"],["l_knee",50,400,"pink"],["r_foot",150,450,"yellow"],["l_foot",50,450,"pink"]]
	with open("test.csv", "w") as f:
		writer = csv.writer(f)
		for parts in parts_list:
			parts_name = "first_"+parts[0]
			print(parts_name)
			x0, y0, x1, y1 = canvas.coords(parts_name)
			print(x0, y0, x1, y1)
			writer.writerow([parts_name,x0, y0, x1, y1])
			parts_name = "second_"+parts[0]
			print(parts_name)
			x0, y0, x1, y1 = canvas.coords(parts_name)
			print(x0, y0, x1, y1)
			writer.writerow([parts_name,x0, y0, x1, y1])

def select_secondImg():
	print("select_secondImg")

def pose_estimate():
	global canvas
	print("pose_estimate")
	#canvas.coords("first_head", 100, 100, 110, 110)
	with open('test.csv') as f:
		reader = csv.reader(f)
		l = [row for row in reader]
	for i in l:
		canvas.coords(str(i[0]), i[1], i[2], i[3], i[4])
	draw_line()




def convert(img):
	image_bgr = img
	image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
	image_pil = Image.fromarray(image_rgb) # RGBからPILフォーマットへ変換
	image_tk  = ImageTk.PhotoImage(image_pil)
	return image_tk


def gui(base_dict_ori,info_dict_ori,first_result_img_ori,second_result_img_ori):

	global info_dict,base_dict,canvas
	global parts_list
	global txt1,txt2,txt3,txt4,B5text,status,first_img_on_canvas,second_img_on_canvas

	info_dict = info_dict_ori
	base_dict = base_dict_ori

	first_img = first_result_img_ori
	second_img = second_result_img_ori

	height = info_dict["height"]
	width = info_dict["width"]
	canvas_width = width
	canvas_height = height
	img_width = info_dict["img_width"]
	img_height = info_dict["img_height"]

	root = tk.Tk()
	root.title("Skeleton2Stroke")
	root.minsize((canvas_width*2)+150,canvas_height+50)
	canvas = tk.Canvas(bg="white", width=(canvas_width*2)+10, height=canvas_height)
	canvas.place(x=140, y=0)

	first_img_label = info_dict["first_img_label"]
	second_img_label = info_dict["second_img_label"]

	parts_list = [["head",100,100,"red"],["r_eye",110,100,"red"],["l_eye",90,100,"red"],["r_ear",130,100,"red"],["l_ear",70,100,"red"],["neck",100,200,"red"],
	["r_shoulder",150,200,"blue"],["l_shoulder",50,200,"green"],["r_elbow",170,230,"blue"],["l_elbow",30,230,"green"],["r_hand",170,260,"blue"],["l_hand",30,260,"green"],
	["r_leg",150,300,"yellow"],["l_leg",50,300,"pink"],["r_knee",150,400,"yellow"],["l_knee",50,400,"pink"],["r_foot",150,450,"yellow"],["l_foot",50,450,"pink"]]

	conv_first_img = convert(first_img)
	first_img_on_canvas = canvas.create_image(0, 0, image=conv_first_img, anchor=tk.NW, tags="first")

	conv_second_img = convert(second_img)
	second_img_on_canvas = canvas.create_image((canvas_width)+10, 0, image=conv_second_img, anchor=tk.NW, tags="second")

	lbl1 = tk.Label(text='index')
	lbl1.place(x=int(canvas_width/2), y=canvas_height+10)
	txt1 = tk.Entry(width=2)
	txt1.place(x=int(canvas_width/2)+40, y=canvas_height+10)
	lbl3 = tk.Label(text='pair')
	lbl3.place(x=int(canvas_width/2)+75, y=canvas_height+10)
	txt3 = tk.Entry(width=2)
	txt3.place(x=int(canvas_width/2)+120, y=canvas_height+10)

	lbl2 = tk.Label(text='index')
	lbl2.place(x=int(canvas_width*3/2), y=canvas_height+10)
	txt2 = tk.Entry(width=2)
	txt2.place(x=(canvas_width*3/2)+40, y=canvas_height+10)
	lbl4 = tk.Label(text='pair')
	lbl4.place(x=int(canvas_width*3/2)+75, y=canvas_height+10)
	txt4 = tk.Entry(width=2)
	txt4.place(x=int(canvas_width*3/2)+120, y=canvas_height+10)

	space = 50
	button_num = 0

	Button1 = tk.Button(text='Frame\nStart',command=select_firstImg,height = 2, width = 8)
	Button1.place(x = 10, y = 10)

	button_num += 1
	Button2 = tk.Button(text='Frame\nEnd',command=select_secondImg,height = 2, width = 8)
	Button2.place(x = 10, y = 10 +space*button_num)

	button_num += 1
	Button3 = tk.Button(text='Pose\nEstimation',command=pose_estimate,height = 2, width = 8)
	Button3.place(x = 10, y = 10 +space*button_num)

	# Button8 = tk.Button(text='Add\nSkeleton',command=add_skelton,height = 2, width = 8)
	# Button8.place(x = 10, y = 10 +space*3)

	button_num += 1
	Button4 = tk.Button(text='Apply\nSkeleton',command=apply_skelton_Information,height = 2, width = 8)
	Button4.place(x = 10, y = 10 +space*button_num)

	button_num += 1
	B5flag = True
	B5text = tk.StringVar()
	B5text.set("Skeleton\nOFF")
	Button5 = tk.Button(textvariable=B5text,command=hide_skelton,height = 2, width = 8)
	Button5.place(x = 10, y = 10 +space*button_num)

	button_num += 1
	Button6 = tk.Button(text='Apply\nCorrection',command=detail_correction,height = 2, width = 8)
	Button6.place(x = 10, y = 10 +space*button_num)

	button_num += 1
	Button7 = tk.Button(text='Finish\nCorrection',command=finish_correction,height = 2, width = 8)
	Button7.place(x = 10, y = 10 +space*button_num)

	button_num += 1
	status = tk.Text(width=15,height=10)
	status.place(x = 10, y = 10 +space*button_num)


	canvas.tag_bind("first", "<ButtonPress-1>", first_pressed)
	canvas.tag_bind("second", "<ButtonPress-1>", second_pressed)

	r = 7
	for parts in parts_list:
		canvas.create_oval(parts[1]*img_width/300-r,parts[2]*img_height/500-r,parts[1]*img_width/300+r,parts[2]*img_height/500+r, fill=parts[3], tags="first_"+parts[0])
	for parts in parts_list:
		canvas.create_oval((canvas_width+10)+parts[1]*img_width/300-r,parts[2]*img_height/500-r,(canvas_width+10)+parts[1]*img_width/300+r,parts[2]*img_height/500+r, fill=parts[3], tags="second_"+parts[0])
	draw_line()

	# クリックされたとき
	canvas.tag_bind("first_head", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_eye", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_eye", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_ear", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_ear", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_neck", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_shoulder", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_shoulder", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_elbow", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_elbow", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_hand", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_hand", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_leg", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_leg", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_knee", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_knee", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_r_foot", "<ButtonPress-1>", pressed)
	canvas.tag_bind("first_l_foot", "<ButtonPress-1>", pressed)

	canvas.tag_bind("second_head", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_eye", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_eye", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_ear", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_ear", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_neck", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_shoulder", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_shoulder", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_elbow", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_elbow", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_hand", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_hand", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_leg", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_leg", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_knee", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_knee", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_r_foot", "<ButtonPress-1>", pressed)
	canvas.tag_bind("second_l_foot", "<ButtonPress-1>", pressed)
	# ドラッグされたとき
	canvas.tag_bind("first_head", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_eye", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_eye", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_ear", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_ear", "<B1-Motion>", dragged)
	canvas.tag_bind("first_neck", "<B1-Motion>", dragged)
	canvas.tag_bind("first_neck", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_shoulder", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_shoulder", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_elbow", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_elbow", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_hand", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_hand", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_leg", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_leg", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_knee", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_knee", "<B1-Motion>", dragged)
	canvas.tag_bind("first_r_foot", "<B1-Motion>", dragged)
	canvas.tag_bind("first_l_foot", "<B1-Motion>", dragged)

	canvas.tag_bind("second_head", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_eye", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_eye", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_ear", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_ear", "<B1-Motion>", dragged)
	canvas.tag_bind("second_neck", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_shoulder", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_shoulder", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_elbow", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_elbow", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_hand", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_hand", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_leg", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_leg", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_knee", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_knee", "<B1-Motion>", dragged)
	canvas.tag_bind("second_r_foot", "<B1-Motion>", dragged)
	canvas.tag_bind("second_l_foot", "<B1-Motion>", dragged)



	root.mainloop()
