import pathlib
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('agg')
import math
import os
import cv2
from scipy.sparse.csgraph import shortest_path
import networkx as nx

from skimage.morphology import skeletonize, thin

import copy

def display(img):
	plt.imshow(img)
	plt.show()

def make_skeleton(img_thre,height,width):
	for y in range(height):
		for x in range(width):
			if img_thre[y,x] == 255:
				img_thre[y,x] = 0
			else:
				img_thre[y,x] = 1

	skeleton = skeletonize(img_thre)

	return skeleton

def preparation_img(img_height,img_width,img_name):
	ori_img = cv2.imread("genga/" + img_name +'.png')
	ori_height, ori_width = ori_img.shape[:2]
	magnification = math.sqrt((ori_height*ori_width)//(img_height*img_width))
	if magnification <= 0:
		magnification = 1

	img = cv2.resize(ori_img , (int(ori_width/magnification), int(ori_height/magnification)))

	height, width = img.shape[:2]

	# グレースケール化
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# 単純二値化
	ret, img_thre = cv2.threshold(img_gray,249, 255,cv2.THRESH_BINARY)

	# スケルトン化
	skeleton= make_skeleton(img_thre,height,width)

	line_img = np.zeros((height, width), np.uint8)
	close_area_img = np.zeros((height, width), np.uint8)

	for y in range(height):
		for x in range(width):
			close_area_img[y,x] = 255

	for y in range(height):
		for x in range(width):
			if skeleton[y,x]:
				close_area_img = cv2.circle(close_area_img, (x,y), 1, 0, thickness=-1)
				line_img = cv2.circle(line_img, (x,y), 1, 255, thickness=-1)

	return height, width,img,skeleton,line_img,close_area_img

def bg_linelabel(height,width,skeleton,close_img_n,close_img_label,close_img_data):
	#bglabel
	temp_size = 0
	bg_label = 0
	for i in range(close_img_n):
		if (close_img_data[i][4])>temp_size:
			temp_size = close_img_data[i][4]
			bg_label = i
	#linelabel
	line_label_list = []
	for y in range(height):
		for x in range(width):
				if (skeleton[y,x]):
					if close_img_label[y,x] not in line_label_list:
						line_label_list.append(close_img_label[y,x])

	return bg_label,line_label_list[0]

def makemask(height,width,img_name,close_img_n,close_img_label):
	labellist = []
	templist = []
	resultlist = []
	#フォルダ作成
	pathlib.Path('./shape%s'%img_name).mkdir(exist_ok=True)
	# 画像を書き込む場所
	img_path = ('./shape%s'%img_name)
	#フォルダあるなし
	LD = os.listdir('./shape%s'%img_name)
	if len(LD) == 0:

		for i in range(close_img_n):
			labellist.append(copy.deepcopy(templist))
		for y in range(height):
			for x in range(width):
				labellist[close_img_label[y,x]].append([y,x])

		result = np.zeros((height, width,3), np.uint8)
		for i in range(close_img_n):
			resultlist.append(copy.deepcopy(result))
			for j in labellist[i]:
				resultlist[i][j[0],j[1]] = (255,255,255)
			cv2.imwrite(os.path.join(img_path,"label%s.png"%i),resultlist[i])
			print("done:" + "label%s"%i)

def make_adjacentlist(base_dict,height,width,img_name,close_img_n,close_img_label,close_img_data,skeleton,bg_label,line_label):
	adjacent_dict = {}
	tempdict = {}

	for i in range(close_img_n):
		tempdict[i] = 0
	for i in range(close_img_n):
		adjacent_dict[i] = copy.deepcopy(tempdict)
	r = 3
	for y in range(r,height-r):
		for x in range(r,width-r):
			if (skeleton[y,x]):
				adjacent_dict[close_img_label[y-r,x-r]][close_img_label[y+r,x+r]] += 1
				adjacent_dict[close_img_label[y+r,x-r]][close_img_label[y-r,x+r]] += 1
				adjacent_dict[close_img_label[y-r,x+r]][close_img_label[y+r,x-r]] += 1
				adjacent_dict[close_img_label[y+r,x+r]][close_img_label[y-r,x-r]] += 1
				adjacent_dict[close_img_label[y-r,x]][close_img_label[y+r,x]] += 1
				adjacent_dict[close_img_label[y+r,x]][close_img_label[y-r,x]] += 1
				adjacent_dict[close_img_label[y,x-r]][close_img_label[y,x+r]] += 1
				adjacent_dict[close_img_label[y,x+r]][close_img_label[y,x-r]] += 1

	for i in range(close_img_n):
		adjacentlist = []
		adjacentdict = {}
		for j in range(close_img_n):
			if adjacent_dict[i][j] != 0 and j != bg_label and j != line_label and i != j:
				adjacentlist.append(j)
				#角度の計算
				adjacentdict["label%s"%j] = math.atan2(close_img_data[i][0] - close_img_data[j][0],close_img_data[i][1] - close_img_data[j][1])* 180 / math.pi

		base_dict[img_name]["label%s"%i]["adjacentlist"] = adjacentdict

def make_result_img(height,width,base_dict,first_img_name,second_img_name,first_img_label,second_img_label):
	first_result_img = np.zeros((height, width,3), np.uint8)
	for y in range(height):
		for x in range(width):
			first_label_name = "label%s"%str(first_img_label[y,x])
			first_result_img[y,x] = (base_dict[first_img_name][first_label_name]["color"][0],base_dict[first_img_name][first_label_name]["color"][1],base_dict[first_img_name][first_label_name]["color"][2])
	second_result_img = np.zeros((height, width,3), np.uint8)
	for y in range(height):
		for x in range(width):
			second_label_name = "label%s"%str(second_img_label[y,x])
			second_result_img[y,x] = (base_dict[second_img_name][second_label_name]["color"][0],base_dict[second_img_name][second_label_name]["color"][1],base_dict[second_img_name][second_label_name]["color"][2])
	return first_result_img,second_result_img

def make_junction_list(height,width,skeleton):
	n = 1
	junction_point = []
	for y in range(0+n,height-n):
		for x in range(0+n,width-n):
			if skeleton[y,x]:
				temp_point = 0
				temp_list = [[y+1,x+1],[y+1,x],[y+1,x-1],[y,x+1],[y,x],[y,x-1],[y-1,x+1],[y-1,x],[y-1,x-1]]
				for i in temp_list:
					if skeleton[i[0],i[1]]:
						temp_point += 1
					if temp_point>=4:
						junction_point.append([y,x])
	arrange(junction_point,2)

	return junction_point

def arrange(list,n):
	new_list = []
	for i in range(len(list)):
		for j in range(i+1,len(list)):
			if (list[j][0]-list[i][0])**2 + (list[j][1]-list[i][1])**2 <= n**2:
				list[j] = [0,0]

def make_divide_line_img(line_img,height,width,skeleton):
	pre_divied_line_img = copy.deepcopy(line_img)
	pre_junction_list = make_junction_list(height,width,skeleton)
	junction_list = []
	for pre_junction in pre_junction_list:
		if pre_junction[0] != 0 and pre_junction[1] != 0:
			junction_list.append(pre_junction)

	for i in junction_list:
		#半径４
		pre_divied_line_img = cv2.circle(pre_divied_line_img, (i[1], i[0]), 4, 255, thickness=-1)
	pre_divied_line_img_n,pre_divied_line_img_label,pre_divied_line_img_data,pre_divied_line_img_center = cv2.connectedComponentsWithStats(pre_divied_line_img)

	omit_list = []
	for i in range(pre_divied_line_img_n):
		if (pre_divied_line_img_data[i][4])<15 or (pre_divied_line_img_data[i][4])>(0.1*height*width):
			omit_list.append(i)

	divied_line_img = np.zeros((height, width), np.uint8)

	for y in range(height):
		for x in range(width):
			if (pre_divied_line_img_label[y,x] not in omit_list):
				divied_line_img[y,x] = 255


	return junction_list,divied_line_img

def coloring_line(height, width,junction_list,colorlist,line_list,divied_line_img_label,divied_line_img_data,close_img_label,bg_label,line_label):
	result = np.zeros((height, width,3), np.uint8)
	for y in range(height):
		for x in range(width):
			result[y,x] = (255,255,255)

	for y in range(height):
		for x in range(width):
			if close_img_label[y,x] == bg_label:
				result[y,x] = (255,255,255)
			elif close_img_label[y,x] == line_label:
				if colorlist[line_list[divied_line_img_label[y,x]][0]][line_list[divied_line_img_label[y,x]][1]][0] == 0:
					colorlist[line_list[divied_line_img_label[y,x]][0],line_list[divied_line_img_label[y,x]][1]] = (np.array([random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]))
					colorlist[line_list[divied_line_img_label[y,x]][1],line_list[divied_line_img_label[y,x]][0]] = colorlist[line_list[divied_line_img_label[y,x]][0],line_list[divied_line_img_label[y,x]][1]]
					result[y,x] = colorlist[line_list[divied_line_img_label[y,x]][0],line_list[divied_line_img_label[y,x]][1]]
				else:
					result[y,x] = colorlist[line_list[divied_line_img_label[y,x]][0],line_list[divied_line_img_label[y,x]][1]]
	for i in junction_list:
		result = cv2.circle(result, (i[1], i[0]), 4, (255,255,255), thickness=-1)
	return result

def make_Situation_list(height,width,junction_list,img_label,img_BGlabel,img_n,img_linelabel):
	r = 5
	#交差点ごとにラベルの面積確認
	junction_img = np.zeros((height, width), np.uint8)

	#円周上の点を決める
	r_img = np.zeros((2*r+1, 2*r+1), np.uint8)
	cv2.circle(r_img, (r, r), r, 255, thickness=1)
	circle_list = []
	for y in range(2*r+1):
		for x in range(2*r+1):
			if r_img[y,x] == 255:
				circle_list.append([y,x])

	junction_dict = {}
	for i in range(len(junction_list)):
		temp_list = []
		temp_dict = {}
		for j in range(len(circle_list)):
			temp = img_label[circle_list[j][0] + junction_list[i][0]-r,circle_list[j][1] + junction_list[i][1]-r]
			if temp != img_linelabel and temp != img_BGlabel:
				temp_list.append(temp)

		for k in temp_list:
			if k in temp_dict:
				temp_dict[k] += 1
			else:
				 temp_dict[k] = 1
		if len(temp_dict.keys()) >1:
			junction_dict[i] = temp_dict

	#グラフの作成
	graph_dict = {}
	graph_temp_list = np.zeros(img_n)
	for i in range(img_n):
		graph_dict[i] = copy.deepcopy(graph_temp_list)

	graph = nx.DiGraph()
	for i in junction_dict.keys():
		for j in junction_dict[i].keys():
			graph.add_node(j)

	print(junction_dict)

	for i in junction_dict.keys():
		temp_list = []
		for h in junction_dict[i].keys():
			temp_list.append(h)
		for j in range(len(temp_list)):
			for k in range(j,len(temp_list)):
				if junction_dict[i][temp_list[j]]-junction_dict[i][temp_list[k]] > 0:
					graph_dict[temp_list[j]][temp_list[k]] = junction_dict[i][temp_list[j]]-junction_dict[i][temp_list[k]]
					#graph_dict[temp_list[k]][temp_list[j]] = -(junction_dict[i][temp_list[j]]-junction_dict[i][temp_list[k]])
				else:
					#graph_dict[temp_list[k]][temp_list[j]] = junction_dict[i][temp_list[j]]-junction_dict[i][temp_list[k]]
					graph_dict[temp_list[j]][temp_list[k]] = -(junction_dict[i][temp_list[j]]-junction_dict[i][temp_list[k]])

		for j in range(img_n):
			for k in range(j,img_n):
				if graph_dict[j][k] > 0:
					graph.add_edge(j,k,weight=graph_dict[j][k])

	depth_score = np.zeros(img_n)

	for i in range(img_n):
		for j in range(i,img_n):
			if graph_dict[i][j] != 0:
				depth_score[j] +=  depth_score[i] + graph_dict[i][j]



	nx.draw_networkx(graph,node_color='red')
	plt.show()

	print(graph_dict)
	print("depth_score",depth_score)

def make_linelist(height,width,close_img_label,close_img_n,divied_line_img_n,divied_line_img_label,skeleton,img_linelabel):
	colorlist = []
	line_dict = {}
	tempdict = {}

	for i in range(close_img_n):
		tempdict[i] = 0
	for i in range(divied_line_img_n):
		line_dict[i] = copy.deepcopy(tempdict)
	r = 3

	for y in range(r,height-r):
		for x in range(r,width-r):
			if (skeleton[y,x]):
				line_dict[divied_line_img_label[y,x]][close_img_label[y+r,x+r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y+r,x-r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y-r,x+r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y-r,x-r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y,x+r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y,x-r]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y+r,x]] += 1
				line_dict[divied_line_img_label[y,x]][close_img_label[y-r,x]] += 1
	for i in range(divied_line_img_n):
		line_dict[i][img_linelabel] = 0
	line_list = []
	print(line_dict)
	for i in range(divied_line_img_n):
		score_sorted = sorted(line_dict[i].items(), key=lambda x:x[1],reverse=True)
		line_list.append([score_sorted[0][0],score_sorted[1][0]])
	for i in line_list:
		i.sort()
	return line_list
