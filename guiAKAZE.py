import cv2
import glob

import guiDict as Dict


akaze = cv2.AKAZE_create()

size_weight = 1

# def matching(base_dict,first_img_name,second_img_name,first_img_data,second_img_data):
# 	first_imgs =glob.glob('shape'+first_img_name+'/*.png')
# 	for j, first_shape_img_name in enumerate(first_imgs):
# 		print(first_shape_img_name)
# 		first_shape_img = cv2.imread(first_shape_img_name)
# 		first_key_points, first_descriptions = akaze.detectAndCompute(first_shape_img, None)
# 		second_imgs =glob.glob('shape'+second_img_name+'/*.png')
# 		for j, second_shape_img_name in enumerate(second_imgs):
# 			second_shape_img = cv2.imread(second_shape_img_name)
# 			score = featuremaching(first_shape_img,second_shape_img,first_descriptions)
# 			first_img_label = str(first_shape_img_name.replace('shape'+first_img_name+'/', '').replace('.png', ''))
# 			second_img_label = str(second_shape_img_name.replace('shape'+second_img_name+'/', '').replace('.png', ''))
# 			sizescore = sizeScore(size_weight,base_dict,int(first_img_label.replace('label', '')),int(second_img_label.replace('label', '')),first_img_data,second_img_data)
# 			score = score * sizescore
# 			Dict.add_score(score,base_dict,first_img_name,second_img_name,first_img_label,second_img_label)

def matching(base_dict,first_img_name,second_img_name,first_img_data,second_img_data):

	first_imgs =glob.glob('shape'+first_img_name+'/*.png')
	first_descriptions_list = []
	for j, first_shape_img_name in enumerate(first_imgs):
		first_shape_img = cv2.imread(first_shape_img_name)
		first_key_points, first_descriptions = akaze.detectAndCompute(first_shape_img, None)
		first_descriptions_list.append(first_descriptions)

	second_imgs =glob.glob('shape'+second_img_name+'/*.png')
	second_descriptions_list = []
	for j, second_shape_img_name in enumerate(second_imgs):
		second_shape_img = cv2.imread(second_shape_img_name)
		second_key_points, second_descriptions = akaze.detectAndCompute(second_shape_img, None)
		second_descriptions_list.append(second_descriptions)

	for i, first_shape_img_name in enumerate(first_imgs):
		for j, second_shape_img_name in enumerate(second_imgs):
			print(first_shape_img_name,second_shape_img_name)
			first_img_label = str(first_shape_img_name.replace('shape'+first_img_name+'/', '').replace('.png', ''))
			second_img_label = str(second_shape_img_name.replace('shape'+second_img_name+'/', '').replace('.png', ''))
			score = featuremaching(first_key_points,first_descriptions_list[i],second_key_points,second_descriptions_list[j],int(first_img_label.replace('label', '')),int(second_img_label.replace('label', '')),first_img_data,second_img_data)
			sizescore = sizeScore(size_weight,base_dict,int(first_img_label.replace('label', '')),int(second_img_label.replace('label', '')),first_img_data,second_img_data)
			score = score * sizescore
			Dict.add_score(score,base_dict,first_img_name,second_img_name,first_img_label,second_img_label)

def sizeScore(size_weight,base_dict,first_img_label,second_img_label,first_img_data,second_img_data):
	sizescore = 1
	big = first_img_data[first_img_label][4]
	small = second_img_data[second_img_label][4]
	if small > big:
		sizescore = big/small
	else:
		sizescore = small/big
	return sizescore*size_weight

def featuremaching(first_key_points,first_descriptions,second_key_points,second_descriptions,first_img_label,second_img_label,first_img_data,second_img_data):
	if first_img_data[first_img_label][4] <= 10 or second_img_data[second_img_label][4] <= 10:
		score = 0
	else:
		bf_matcher = cv2.BFMatcher()
		# print(len(first_descriptions),len(first_descriptions))
		matches = bf_matcher.knnMatch(first_descriptions, second_descriptions, k=2)
		ratio = 0.8
		good = []
		for m in matches:
			if len(m)==1:
				continue
			n = m[1]
			m = m[0]
			if m.distance < ratio * n.distance:
				good.append([m])
		good = sorted(good, key=lambda x: x[0].distance)
		score = len(good)*10
	return score
