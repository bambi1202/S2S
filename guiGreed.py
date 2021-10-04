import guiDict as Dict

def greed(greed_weight,base_dict,first_img_name,second_img_name):
	seedlist = []
	seedlist = findSeed(base_dict,first_img_name,second_img_name)
	print(seedlist)
	greedmatching(base_dict,seedlist[0],seedlist[1],first_img_name,second_img_name)
	Dict.set_pair(base_dict,first_img_name,second_img_name)

def findSeed(base_dict,first_img_name,second_img_name):
	seedlist = [0,0]
	score = 0
	for label in (base_dict[first_img_name]):
		if base_dict[second_img_name][base_dict[first_img_name][label]["pair"]]["pair"] == label:
			print(str(label) + ":" + str(base_dict[first_img_name][label]["pair"]))
			tmpscore = base_dict[first_img_name][label]["score"][base_dict[first_img_name][label]["pair"]]
			if tmpscore > score and 10000>tmpscore:
				seedlist[0] = (label)
				seedlist[1] = (base_dict[first_img_name][label]["pair"])
				score = tmpscore
	return seedlist

def greedmatching(base_dict,first_img_seed,second_img_seed,first_img_name,second_img_name):
	seed_bounus = 10000
	Dict.add_score(seed_bounus,base_dict,first_img_name,second_img_name,first_img_seed,second_img_seed)

	first_img_seed_adjacent_list = []
	for i in (base_dict[first_img_name][first_img_seed]["adjacentlist"].keys()):
		first_img_seed_adjacent_list.append(i)

	second_img_seed_adjacent_list = []
	for i in (base_dict[second_img_name][second_img_seed]["adjacentlist"].keys()):
		second_img_seed_adjacent_list.append(i)

	#角度
	for i in first_img_seed_adjacent_list:
			for j in second_img_seed_adjacent_list:
				recent_first_label_angle = base_dict[first_img_name][first_img_seed]["adjacentlist"][i]
				recent_second_label_angle = base_dict[second_img_name][second_img_seed]["adjacentlist"][j]
				angledef = (abs(recent_first_label_angle-recent_second_label_angle))%360
				if angledef>180:
					angledef = 360-angledef
				recent_score = (1+((180-angledef)/180))**2
				print("recent_score = " + str(recent_score))

				Dict.multiply_score(recent_score,base_dict,first_img_name,second_img_name,i,j)
		# #深さ
		# for i in first_templist:
		# 	for j in second_templist:
		# 		if (base_dict[first_img_name][i]["depth"] - base_dict[first_img_name][first_img_seed]["depth"]>=0):
		# 			first_depth_flag = 1
		# 		else:
		# 			first_depth_flag = 0

		# 		if (base_dict[second_img_name][j]["depth"] - base_dict[second_img_name][second_image_seed]["depth"]>=0):
		# 			second_depth_flag = 1
		# 		else:
		# 			second_depth_flag = 0
		#
		# 		if (first_depth_flag == second_depth_flag):
		# 			recent = 1*(1+depth_weight)
		# 		else:ß
