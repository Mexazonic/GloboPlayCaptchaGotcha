import cv2
import numpy as np
from matplotlib import pyplot as plt

origin = cv2.imread('captchas/download.png') #download.png works! Another image got some problems 
gray = cv2.imread('captchas/download.png', 0) # Open image in gray scale

image = gray.copy()

cv2.imshow('original', origin)
cv2.waitKey(0) 

#cv2.imshow('gray before', gray)

gray = cv2.bitwise_not(image) #bit a bit analyse to take roi(region of image)
bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2) # negative (black and white image)

#cv2.imshow('gray after', gray)
#cv2.imshow('bw', bw)
#cv2.waitKey(0) 

"""
#### Horizontal Lines Extract ####
# Specify size on horizontal axis
horizontalines = np.copy(bw)
cols = horizontalines.shape[1]
horizontal_size = cols // 7

# Create structure element for extracting horizontal lines through morphology operations
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

# Apply morphology operations
horizontal_eroded = cv2.erode(gray, horizontalStructure)
horizontal_dilated = cv2.dilate(horizontal_eroded, horizontalStructure)

cv2.imshow('lines', horizontal_dilated)
cv2.waitKey(0)
#### Horizontal Lines Extract ####
""" 

### Vertical (Symbol) Extract ###
vertical = np.copy(bw)
#cv2.imshow('vertical', vertical) #black and white

# Specify size on vertical axis
rows = vertical.shape[0]
verticalsize = 2
# Create structure element for extracting vertical lines through morphology operations
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
# Apply morphology operations
vertical = cv2.erode(gray, verticalStructure)
vertical = cv2.dilate(vertical, verticalStructure)
# Show extracted vertical lines
#show_wait_destroy("vertical", vertical)

cv2.imshow('symbol', vertical)
cv2.waitKey(0)
### Vertical (Symbol) Extract ###



img = cv2.bitwise_not(vertical) #image without horizontal lines (black turn white) roi black  
original = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) #grayscale to a rgb channel
reverse = cv2.cvtColor(vertical,cv2.COLOR_GRAY2BGR)	#reverse in rgb

cv2.imshow('img', img)
cv2.imshow('orig',original) #note: conflict name cv2.imshow
#cv2.imshow('reverse', reverse)
#cv2.waitKey(0)

#raw_image = img #image in bw channel -> raws symbols
raw_image = original
# image is the new symbol in 
image = original 

# Grayscale 

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
#cv2.imshow('gray', gray)
# Find Canny edges 


edged = cv2.Canny(gray, 30, 200) #lapping edges
#edged = cv2.Canny(img, 30, 200) #same efect 
#cv2.imshow('ed', edged) 


# Finding Contours 
contours, hierarchy = cv2.findContours(edged, 
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

cv2.imshow('Edges After Contouring', edged) 
cv2.waitKey(0) 

print("Number of Contours found = " + str(len(contours))) 

"""
# Draw all contours (Optional) 
# -1 signifies drawing all contours 
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
#cv2.imshow('Contours', image) 
#cv2.waitKey(0) 
"""

check = reverse
img =  reverse
#mask = np.zeros_like(reverse) # Create mask where white is what we want, black otherwise
mask = img
#cv2.imshow('O Mascara antes', mask )
#cv2.waitKey(0)

i = 0
while i < len(contours):
	cv2.drawContours(mask, contours, i , 255, -1) # Draw filled contour in mask
	i+=1

#cv2.imshow('O Mascara depois', mask )
#cv2.waitKey(0)

out = np.zeros_like(img) # Extract out the object and place into output image (return array in 0's 0 -> black)
#cv2.imshow('mask',out)
#cv2.waitKey(0)

out[mask == 255] = img[mask == 255] #hack

#cv2.imshow('mask',out)
#cv2.waitKey(0)


#take roi coordinates
y, x = np.where(gray == 255)

(topy, topx) = (np.min(y), np.min(x))

(bottomy, bottomx) = (np.max(y), np.max(x))

out = out[topy:bottomy+1, topx:bottomx+1]

#print(topx, topy, bottomx, bottomy)

# Show the output image
#cv2.imwrite('im.png', out)
cv2.imshow('Output', out)
cv2.waitKey(0)

"""#Optional Contourns Detection
mx = (0,0,0,0)
mx_area = 0

print('contourns: %s' % len(contours))

for cont in contours:
	x, y, w, h = cv2.boundingRect(cont)
	area = w*h
	if area > mx_area:
		mx = x, y, w, h
		mx_area = area
				
x, y, w, h = mx
print(x, y, w, h)
"""

xywh = list()
option_size = 20


for cont in contours:
	x, y, w, h = cv2.boundingRect(cont)
	#area = w*h
	
	if(h < option_size and w < option_size):
		continue
	
	#print('testing: ', x, y, w, h)
	
	roi = img[y:y+h, x:x+w]
	#cv2.imwrite('IMAGE_CROP.jpg', roi)
	xywh.append(x)
	xywh.append(y)
	xywh.append(w)
	xywh.append(h)
	#print(xywh)
	#print(coordinate[0])
	#cv2.imshow('IMAGE_CROP.jpg', roi)
	#print('try: ', coordinate)
	#cv2.waitKey(0)


j = 4 #split elements size
coordinates = [xywh[i:i + j] for i in range(0, len(xywh), j)] #split list in 4 params for coordinates: list -> matrix

#Coordinates shape: x, y, w, h 
"""
if area > mx_area:
	mx = x, y, w, h
	mx_area = area
	x, y, w, h = mx
	print('==========================')
	print('testing: ', x, y, w, h)
	#roi = img[y:y+34, x:x+30]
	roi = img[y:y+h, x:x+w]
	#cv2.imwrite('IMAGE_CROP.jpg', roi)
	cv2.imshow('IMAGE_CROP.jpg', roi)
	cv2.waitKey(0)
"""
#print(range(5))

for i in range(len(coordinates)):
	#print(coordinate)
	#roi = img[y:y+34, x:x+30]
	x = coordinates[i][0] 
	y = coordinates[i][1] 
	w = coordinates[i][2] 
	h = coordinates[i][3]
	roi = raw_image[y:y+h, x:x+w]
	cv2.imwrite('elements/IMAGE_CROP' + str(i) + '.jpg', roi)
	cv2.imshow('single_element.jpg', roi)
	cv2.waitKey(0)

i = 2 #manual select image (range: [0, 4])
x = coordinates[i][0] 
y = coordinates[i][1] 
w = coordinates[i][2] 
h = coordinates[i][3]
cv2.rectangle(origin,(x,y), (x+w, y+h), (200,0,0), 2)
cv2.imwrite('gotcha/select_box.jpg',origin )
cv2.imshow('IMAGE_board.jpg',origin)
cv2.waitKey(0)
