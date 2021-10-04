import copy
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cv2

def depthlist(height,width,dn,r,img,img_ori,thresh,label_ori,n_ori,Linelabel_ori,BGlabel_ori,center_ori):
	pointlist = []
	deepdict = {}
	mylabel = -1
	#display(thresh)
	for y in range(0, int(height)):
		for x in range(0, int(width)):
			if x%dn==0 and y%dn==0:
				if thresh[y,x] == 0:
					if label_ori[y,x] != mylabel:
						mylabel = label_ori[y,x]
					else:
						pointlist.append([x,y])
	#print(len(pointlist))

	for i in range(0,len(pointlist)):
		for y in range(pointlist[i][1]-r if pointlist[i][1]-r >0 else 0,pointlist[i][1]+r if pointlist[i][1]+r < height else height):
			for x in range(pointlist[i][0]-r if pointlist[i][0]-r >0 else 0,pointlist[i][0]+r if pointlist[i][0]+r < width else width):
				if ((pointlist[i][1] - y)**2+(pointlist[i][0]-x)**2)<=(r**2):
					if i in deepdict:
						if label_ori[y,x] != Linelabel_ori:
							if label_ori[y,x] in deepdict[i]:
								deepdict[i][label_ori[y,x]] += 1
							else:
								deepdict[i][label_ori[y,x]] = 1
					else:
						deepdict[i] = {"center":"1"}
						deepdict[i].pop("center")

	for i in range(0,len(pointlist)):
		if len(deepdict[i])<3:
			deepdict.pop(i)

	junclist = deepdict.keys()
	r = r+5
	img_point = copy.deepcopy(img)
	# for i in range(n_ori):
	# 	font = cv2.FONT_HERSHEY_SIMPLEX
	# 	cv2.putText(img_point,str(i),(int(center_ori[i][0]),int(center_ori[i][1])), font, 0.5,(255,0,0),2,cv2.LINE_AA)
	# #display(img_point)
    #
	# for i in junclist:
	# 	img_point = cv2.circle(img_point, (pointlist[i][0],pointlist[i][1]), r, (255, 0, 0), thickness=-1)
	# #display(img_point)

	deepdict2 = {}

	for i in junclist:
		for y in range(pointlist[i][1]-r if pointlist[i][1]-r >0 else 0,pointlist[i][1]+r if pointlist[i][1]+r < height else height):
			for x in range(pointlist[i][0]-r if pointlist[i][0]-r >0 else 0,pointlist[i][0]+r if pointlist[i][0]+r < width else width):
				if ((pointlist[i][1] - y)**2+(pointlist[i][0]-x)**2)<=(r**2):
					if i in deepdict2:
						if label_ori[y,x] != Linelabel_ori:
							if label_ori[y,x] in deepdict2[i]:
								deepdict2[i][label_ori[y,x]] += 1
							else:
								deepdict2[i][label_ori[y,x]] = 1
					else:
						deepdict2[i] = {"center":"1"}
						deepdict2[i].pop("center")
	tenplist =[]
	scorelist = []

	for i in range(n_ori-1):
		tenplist.append(0)
	for i in range(n_ori-1):
		c = copy.deepcopy(tenplist)
		scorelist.append(c)

	for i in deepdict.keys():
		for j in (deepdict[i]):
			for k in (deepdict[i]):
				if j!=k:
					scorelist[j-1][k-1] = scorelist[j-1][k-1] + deepdict[i][j]-deepdict[i][k]
					scorelist[k-1][j-1] = scorelist[k-1][j-1] + deepdict[i][k]-deepdict[i][j]

	for i in range(len(scorelist)):
		for j in range(len(scorelist[i])):
			if (scorelist[i][j])<0:
				scorelist[i][j] = 0

	graph = nx.DiGraph()

	for i in range(1,len(scorelist)):
		graph.add_node(i)

	for i in range(1,len(scorelist)):
		for j in range(1,len(scorelist[i])):
			if (scorelist[i][j]) != 0:
				graph.add_edge(i, j, weight=scorelist[i][j])

	for i in nx.simple_cycles(graph):
		mini = 10000
		for j in range(len(i)):
			temp = (scorelist[i[j]][i[(j+1)%len(i)]])
			if temp < mini:
				tempnum= i[j]
				tempnum2 = i[(j+1)%len(i)]
		scorelist[tempnum][tempnum2] = 0

	nx.draw_networkx(graph,node_color='red')
	#plt.show()

	#print(np.array(scorelist))
	depthlist = np.zeros(len(scorelist))
	templist = np.zeros(len(scorelist))

	for i in range(1,len(scorelist)):
		for j in range(len(scorelist[i])):
			if scorelist[i][j]>0:
				depthlist[j] = 1

	depth = 0
	while (depth in depthlist):
		for i in range(1,len(depthlist)):
			if depthlist[i] == depth:
				for j in range(1,len(scorelist[i])):
					if scorelist[i][j] != 0:
						depthlist[j] = depth + 1
		depth += 1

	result = copy.deepcopy(img_ori)
	result = cv2.resize(result , (int(width), int(height)))
	for y in range(0, int(height)):
		for x in range(0, int(width)):
			if label_ori[y,x] != Linelabel_ori and label_ori[y,x] != BGlabel_ori:
				result[y,x] = [int(255-(depthlist[label_ori[y,x]-1])*50),0,0]
			else:
				result[y,x] = [0, 0, 0]

	return result,depthlist
