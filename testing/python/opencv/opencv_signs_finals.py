import cv2
import numpy as np
from matplotlib import pyplot as plt
from operator import itemgetter 

class Sign(object): 
	
	def __init__(self, image, name, short, minHue, minSat, minBr, maxHue, maxSat, maxBr):
		self.name = name
		self.short = short
		self.image = image
		self.minHue = minHue
		self.minSat = minSat
		self.minBr = minBr
		self.maxHue = maxHue
		self.maxSat = maxSat
		self.maxBr = maxBr


cap = cv2.VideoCapture('http://10.0.2.3:8081/')
if (not cap.isOpened()):
	video = "dot_tracking.mp4"
	cap = cv2.VideoCapture(video)


#check_image = cap.read()
#check_image = cv2.imread("new_signs.png")

#img3 = check_image
#hsv = cv2.cvtColor(check_image, cv2.COLOR_BGR2HSV)
#check_image = cv2.cvtColor(check_image, cv2.COLOR_BGR2GRAY)
	
sign_list = []
		
sign_list.append(Sign("templates/template1(2).png", "Oxidizer", "Ox", 20, 0, 0, 35, 255, 255))#1
sign_list.append(Sign("templates/template2.jpg", "Organic Peroxide", "OP", 0, 100, 200, 255, 255, 255))#2
sign_list.append(Sign("templates/template3.png", "Flammable Gas", "FG", 0, 0, 0, 255, 255, 255))#3
sign_list.append(Sign("templates/template4.png", "Inhalation Hazard", "IN", 0, 0, 0, 255, 10, 255))	 #4
sign_list.append(Sign("templates/template5.jpg", "Dangerous When Wet", "DWW", 80, 0, 0, 155, 255, 255))#5
sign_list.append(Sign("templates/template6.jpg", "Flammable Solid", "FS", 0, 0, 0, 255, 255, 255))#6
sign_list.append(Sign("templates/template7.jpg", "Spontaneously Combustible", "SP", 0, 80, 200, 255, 221, 255))#7
sign_list.append(Sign("templates/template8.png", "Explosives", "Ex", 0, 100, 200, 255, 255, 255))#8
sign_list.append(Sign("templates/template9.png", "Radioactive II", "Rad", 0, 100, 200, 255, 255, 255))#9
sign_list.append(Sign("templates/template10.png", "Corrosive", "Cor", 0, 0, 0, 255, 255, 255))#10
sign_list.append(Sign("templates/template11.jpg", "Non-flammable Gas", "NFG", 0, 0, 0, 255, 255, 255))#11
sign_list.append(Sign("templates/template12.png", "Infectious Substance", "IS", 0, 0, 0, 255, 10, 255))#12

'''
lowest distance = 100
loop through rotations
	get match
	if lower, set lowest distance

return lowest
'''

def rotate(sign):
	closest_distance = 100
	for i in range(9):
		dist = match(sign, rotate=45*i)
		if (dist < closest_distance):
			closest_distance = dist
	return closest_distance
		

def match(sign, rotate=-1, debug=False):
	global img3
	
	
	sign_image = cv2.imread(sign.image)
	
	sign_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2GRAY)
	
	#increase contrast
	contrast_image = cv2.equalizeHist(sign_image)
	
	#cv2.imshow("contrast", contrast_image)
	#mask = cv2.inRange(hsv, np.array([sign.minHue, sign.minSat, sign.minBr]), np.array([sign.maxHue, sign.maxSat, sign.maxBr]))
	#res = cv2.bitwise_and(check_image,check_image, mask= mask)
	#No HSV
	res = check_image
	
	#res = sign_image
	
	if not (rotate == -1):
		num_rows, num_cols = sign_image.shape[:2]
		rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), rotate, 1)
		sign_image = cv2.warpAffine(sign_image, rotation_matrix, (num_cols, num_rows))

	orb = cv2.ORB_create()
	kp1, des1 = orb.detectAndCompute(res,None)
	kp2, des2 = orb.detectAndCompute(sign_image,None)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)

	img3 = cv2.drawMatches(res,kp1,check_image,kp2,matches[:1],None, flags=2)

	img1_kp1 = matches[0].queryIdx
	(x1, y1) = kp1[img1_kp1].pt
	#print((int(x1), int(y1)))
	#print (matches[0].distance)
	#if(matches[0].distance < 36):
		#cv2.imshow("matches", cv2.imread(sign.image))

	
	#img3 = cv2.circle(img3,(int(x1), int(y1)), 15, (255,0,0), 2)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	img3 = cv2.putText(img3,sign.short,(int(x1),int(y1)), font, 1, (200,255,155), 2, cv2.LINE_AA)
	
	
	cv2.imshow("match", img3)
	
	if (debug):
		print(sign.name)
		cv2.imshow("res", res)
		cv2.imshow("template", cv2.imread(sign.image))
	
	
	
	return matches[0].distance
	
while (1):
	(grabbed, check_image) = cap.read()
	#print(check_image)
	#hsv = cv2.cvtColor(check_image, cv2.COLOR_BGR2HSV)
	#check_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	
	sign_distances = {}

	for sign in sign_list:
		distance = match(sign)
		rotated_distance = rotate(sign)
		if (distance > rotated_distance):
			distance = rotated_distance
		sign_distances[sign] = distance

	list_keys = []

	for sign, distance in sorted(sign_distances.items(), key=itemgetter(1), reverse=False):
		list_keys.append(sign)
		print(sign.name + ": " + str(distance)) 


	cv2.imshow("Found {}:".format(list_keys[0].name), cv2.imread(list_keys[0].image))
	cv2.imshow("Found {}:".format(list_keys[1].name), cv2.imread(list_keys[1].image))	
	cv2.imshow("Found {}:".format(list_keys[2].name), cv2.imread(list_keys[2].image))
	cv2.imshow("Found {}:".format(list_keys[3].name), cv2.imread(list_keys[3].image))
	
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break
	if key == 27:
		break
		
#match(sign_list[2], False, True)

 

#>>> for k, v in s:
#...     k, 

'''
Dictionary ( Sign >>> Distance )
Loop through all signs
	Match and store distance
	Rotate 180 and match again
	Store lowest distance

Sort dictionary by values (distance)
'''



	
		
