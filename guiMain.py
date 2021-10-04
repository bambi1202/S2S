import sys
import os
import cv2

import copy
import time

import guiImg as Img
import guiDict as Dict
import guiDepth as Depth
import guiCommon as Common
import guiAKAZE as AKAZE
import guiGreed as Greed
import guiTikiner3 as GUI


def main(first_img_name,second_img_name):
	size_weight = 1
	greed_weight = 100

	img_height= 400
	img_width = 1.6*img_height

	#first_img_name = args[1]
	#second_img_name = args[2]

	height,width,first_img,first_skeleton,first_line_img,first_close_area_img = Img.preparation_img(img_height,img_width,first_img_name)
	height,width,second_img,second_skeleton,second_line_img,second_close_area_img = Img.preparation_img(img_height,img_width,second_img_name)

	first_img_ori = copy.deepcopy(first_img)
	second_img_ori = copy.deepcopy(second_img)

	first_img_thre = first_close_area_img
	second_img_thre = second_close_area_img

	first_img_n, first_img_label, first_img_data, first_img_center = cv2.connectedComponentsWithStats(first_img_thre)
	second_img_n, second_img_label, second_img_data, second_img_center = cv2.connectedComponentsWithStats(second_img_thre)

	print(first_img_n)
	print(second_img_n)

	#線と背景のラベル推定
	first_img_BGlabel,first_img_linelabel= Img.bg_linelabel(height,width,first_skeleton,first_img_n,first_img_label,first_img_data)
	second_img_BGlabel,second_img_linelabel = Img.bg_linelabel(height,width,second_skeleton,second_img_n,second_img_label,second_img_data)

	#細線化
	first_junction_list,first_divied_line_img = Img.make_divide_line_img(first_img_thre,height,width,first_skeleton)
	second_junction_list,second_divied_line_img = Img.make_divide_line_img(second_img_thre,height,width,second_skeleton)

	#Img.display(first_divied_line_img)
	first_divied_line_img_n, first_divied_line_img_label, first_divied_line_img_data, first_divied_line_img_center = cv2.connectedComponentsWithStats(first_divied_line_img)
	second_divied_line_img_n, second_divied_line_img_label, second_divied_line_img_data, second_divied_line_img_center = cv2.connectedComponentsWithStats(second_divied_line_img)

	print(first_divied_line_img_n)
	print(second_divied_line_img_n)

	#閉領域情報のdict作成
	base_dict = Dict.make_dict(first_img_name,second_img_name,first_img_n,second_img_n)

	#閉領域の深度推定
	#first_depth_result_img,first_depth_list = Depth.depthlist(height, width,5,10,first_img,first_img_ori,first_img_thre,first_img_label,first_img_n,first_img_linelabel,first_img_BGlabel,first_img_center)
	#second_depth_result_img,second_depth_list = Depth.depthlist(height, width,5,10,second_img,second_img_ori,second_img_thre,second_img_label,second_img_n,second_img_linelabel,second_img_BGlabel,second_img_center)

	#閉領域のマスク作成
	Img.makemask(height,width,first_img_name,first_img_n,first_img_label)
	Img.makemask(height,width,second_img_name,second_img_n,second_img_label)
	Img.make_adjacentlist(base_dict,height,width,first_img_name,first_img_n,first_img_label,first_img_data,first_skeleton,first_img_BGlabel,first_img_linelabel)
	Img.make_adjacentlist(base_dict,height,width,second_img_name,second_img_n,second_img_label,second_img_data,second_skeleton,second_img_BGlabel,second_img_linelabel)
	displayTime()
	#閉領域同士のマッチング
	AKAZE.matching(base_dict,first_img_name,second_img_name,first_img_data,second_img_data)
	displayTime()
	Dict.set_pair(base_dict,first_img_name,second_img_name)
	# print(base_dict)
	#線と背景の設定
	base_dict[first_img_name]["label%s"%str(first_img_BGlabel)]["color"] = [255,255,255]
	base_dict[first_img_name]["label%s"%str(first_img_linelabel)]["color"] = [0,0,0]
	Dict.add_score(100000,base_dict,first_img_name,second_img_name,"label%s"%str(first_img_BGlabel),"label%s"%str(second_img_BGlabel))
	Dict.add_score(100000,base_dict,first_img_name,second_img_name,"label%s"%str(first_img_linelabel),"label%s"%(second_img_linelabel))

	#前後関係推定
	#Img.make_Situation_list(height,width,first_junction_list,first_img_label,first_img_BGlabel,first_img_n,first_img_linelabel)

	#貪欲法
	for i in range(3):
		Greed.greed(greed_weight,base_dict,first_img_name,second_img_name)
	#print(base_dict)

	first_result_img,second_result_img = Img.make_result_img(height,width,base_dict,first_img_name,second_img_name,first_img_label,second_img_label)

	info_dict = make_info_dict(height,width,img_height,img_width,first_img_name,second_img_name,first_result_img,second_result_img,first_img_label,second_img_label,greed_weight,base_dict,first_img_linelabel,first_img_BGlabel,second_img_linelabel,second_img_BGlabel
	,first_divied_line_img_n, first_divied_line_img_label, first_divied_line_img_data, first_divied_line_img_center,second_divied_line_img_n, second_divied_line_img_label, second_divied_line_img_data, second_divied_line_img_center,
	first_junction_list,first_divied_line_img,second_junction_list,second_divied_line_img,first_skeleton,second_skeleton,first_img_n,second_img_n)

	#GUI.GUI(height,width,img_height,img_width,first_img_name,second_img_name,first_result_img,second_result_img,first_img_label,second_img_label,greed_weight,base_dict,first_img_linelabel,first_img_BGlabel,second_img_linelabel,second_img_BGlabel,info_dict)
	GUI.gui(base_dict,info_dict,first_result_img,second_result_img)


	displayTime()

	#--------------------------------------------------------------

def displayTime():
	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

def make_info_dict(height,width,img_height,img_width,first_img_name,second_img_name,first_result_img,second_result_img,first_img_label,second_img_label,greed_weight,base_dict,first_img_linelabel,first_img_BGlabel,second_img_linelabel,second_img_BGlabel
,first_divied_line_img_n, first_divied_line_img_label, first_divied_line_img_data, first_divied_line_img_center,second_divied_line_img_n, second_divied_line_img_label, second_divied_line_img_data, second_divied_line_img_center,
first_junction_list,first_divied_line_img,second_junction_list,second_divied_line_img,first_skeleton,second_skeleton,first_img_n,second_img_n):
	info_dict = {}
	info_dict["height"] = height
	info_dict["width"] = width
	info_dict["img_height"] = img_height
	info_dict["img_width"] = img_width
	info_dict["first_img_name"] = first_img_name
	info_dict["second_img_name"] = second_img_name
	info_dict["first_result_img"] = first_result_img
	info_dict["second_result_img"] = second_result_img
	info_dict["first_img_label"] = first_img_label
	info_dict["second_img_label"] = second_img_label
	info_dict["first_img_linelabel"] = first_img_linelabel
	info_dict["first_img_BGlabel"] = first_img_BGlabel
	info_dict["second_img_linelabel"] = second_img_linelabel
	info_dict["second_img_BGlabel"] = second_img_BGlabel
	info_dict["first_divied_line_img_n"] = first_divied_line_img_n
	info_dict["first_divied_line_img_label"] = first_divied_line_img_label
	info_dict["first_divied_line_img_data"] = first_divied_line_img_data
	info_dict["first_divied_line_img_center"] = first_divied_line_img_center
	info_dict["second_divied_line_img_n"] = second_divied_line_img_n
	info_dict["second_divied_line_img_label"] = second_divied_line_img_label
	info_dict["second_divied_line_img_data"] = second_divied_line_img_data
	info_dict["second_divied_line_img_center"] = second_divied_line_img_center
	info_dict["first_junction_list"] = first_junction_list
	info_dict["first_divied_line_img"] = first_divied_line_img
	info_dict["second_junction_list"] = second_junction_list
	info_dict["second_divied_line_img"] = second_divied_line_img
	info_dict["first_skeleton"] = first_skeleton
	info_dict["second_skeleton"] = second_skeleton
	info_dict["first_img_n"] = first_img_n
	info_dict["second_img_n"] = second_img_n
	info_dict["greed_weight"] = greed_weight
	return info_dict

args = sys.argv
start = time.time()

if __name__ == "__main__":
	main()
