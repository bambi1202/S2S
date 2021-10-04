import copy
import random

def make_dict(first_img_name,second_img_name,first_img_n,second_img_n):
	base_dict = {}
	temp_dict3 = {}
	temp_dict = {}
	temp_dict2 = {}
	for i in range(second_img_n):
		label_name = "label"+str(i)
		temp_dict3[label_name] = 0
	for i in range(second_img_n):
		temp_dict2["score"] = copy.deepcopy(temp_dict3)
	for i in range(first_img_n):
		label_name = "label"+str(i)
		temp_dict[label_name] = copy.deepcopy(temp_dict2)
		temp_dict[label_name]["color"] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
	base_dict[first_img_name] = copy.deepcopy(temp_dict)

	temp_dict = {}
	temp_dict2 = {}
	for i in range(first_img_n):
		label_name = "label"+str(i)
		temp_dict3[label_name] = 0
	for i in range(first_img_n):
		temp_dict2["score"] = copy.deepcopy(temp_dict3)
	for i in range(second_img_n):
		label_name = "label"+str(i)
		temp_dict[label_name] = copy.deepcopy(temp_dict2)
		temp_dict[label_name]["color"] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
	base_dict[second_img_name] = copy.deepcopy(temp_dict)

	return base_dict

def add_score(score,base_dict,first_img_name,second_img_name,first_img_label,second_img_label):
	base_dict[first_img_name][first_img_label]["score"][second_img_label] += score
	base_dict[second_img_name][second_img_label]["score"][first_img_label] += score

def multiply_score(score,base_dict,first_img_name,second_img_name,first_img_label,second_img_label):
	base_dict[first_img_name][first_img_label]["score"][second_img_label] *= score
	base_dict[second_img_name][second_img_label]["score"][first_img_label] *= score

def set_pair(base_dict,first_img_name,second_img_name):
	for label in (base_dict[first_img_name].keys()):
		tempdic = {}
		tempdic = sorted(base_dict[first_img_name][label]["score"].items(), key=lambda x:x[1],reverse=True)
		base_dict[first_img_name][label]["pair"] = tempdic[0][0]

	for label in (base_dict[second_img_name].keys()):
		tempdic = {}
		tempdic = sorted(base_dict[second_img_name][label]["score"].items(), key=lambda x:x[1],reverse=True)
		base_dict[second_img_name][label]["pair"] = tempdic[0][0]
		base_dict[second_img_name][label]["color"] = base_dict[first_img_name][tempdic[0][0]]["color"]

	for label in (base_dict[first_img_name].keys()):
		print(str(first_img_name) + ":" +str(label) + ":" + str(base_dict[first_img_name][label]["pair"])+ "=" + str(base_dict[first_img_name][label]["score"][str(base_dict[first_img_name][label]["pair"])]))
	for label in (base_dict[second_img_name].keys()):
		print(str(second_img_name) + ":" +str(label) + ":" + str(base_dict[second_img_name][label]["pair"])+ "=" + str(base_dict[second_img_name][label]["score"][str(base_dict[second_img_name][label]["pair"])]))
