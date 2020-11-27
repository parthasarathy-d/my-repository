

import numpy as np
import cv2
import csv


def applyPerspectiveTransform(input_img):
    	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

    warped_img = None

    input_img_gray  = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    input_img_gray = np.float32(input_img_gray);
    
    dst = cv2.cornerHarris(input_img_gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),250,0)
    dst = np.uint8(dst)

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(input_img_gray,np.float32(centroids),(5,5),(-1,-1),criteria)


    rect = np.zeros((4, 2), dtype = "float32")

    s = corners.sum(axis = 1)
    rect[0] = corners[np.argmin(s)]
    rect[3] = corners[np.argmax(s)]

    diff = np.diff(corners, axis = 1)
    rect[1] = corners[np.argmin(diff)]
    rect[2] = corners[np.argmax(diff)]
    pts1 = np.float32([rect[0],rect[1],rect[2],rect[3]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)

    wraped_img = cv2.warpPerspective(input_img_gray,M,(300,300))

    ret,warped_img = cv2.threshold(wraped_img,127,255,cv2.THRESH_BINARY)
    warped_img = warped_img.astype(np.uint8)
    _, countours, _ = cv2.findContours(warped_img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in countours:
        cv2.drawContours(warped_img, [contour], 0, (0, 0, 255), 3)


    warped_img = np.array(warped_img)


    return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""


    maze_array = []

    h, w = warped_img.shape
    M = h//10
    N = w//10

    z = 0
    i = -1
    for y in range (0,h,M):
        maze_array.append([])
        i += 1
        y1 = y + M
        for x in range (0,w,N):
            west, north, east, south = 0, 0, 0, 0
            x1 = x + N
            tiles = warped_img[y:y1,x:x1]
            
            nim = np.array(tiles)
            left = [first[0] for first in nim]
            top = nim[0]
            right = [last[29] for last in nim]
            bottom = nim[29]
            
            if np.average(left) == 0:
                west = 1
            if np.average(top) == 0:
                north = 2
            if np.average(right) == 0:
                east = 4
            if np.average(bottom) == 0:
                south = 8

            z = west + north + east + south
            maze_array[i].append(z)
            
    return maze_array


def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":
    
        img_file_path = "maze00.jpg"
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()

