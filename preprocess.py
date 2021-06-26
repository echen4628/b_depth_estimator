from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import random as rng
# the commented out code is from https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
# rng.seed(12345)


# def thresh_callback(val):
#     threshold = val
    
#     canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    
    
#     contours, hierachy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    
#     contours_poly = [None]*len(contours)
#     boundRect = [None]*len(contours)
#     #centers = [None]*len(contours)
#     #radius = [None]*len(contours)
#     for i, c in enumerate(contours):
#         contours_poly[i] = cv.approxPolyDP(c, 3, True)
#         boundRect[i] = cv.boundingRect(contours_poly[i])
#         #centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    
    
#     drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
#     for i in range(len(contours)):
#         color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
#         #cv.drawContours(drawing, contours_poly, i, color)
#         cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
#           (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
#         #cv.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
    
#     print("boundRect: ",boundRect)
    
#     cv.imshow('Contours', drawing)
    

# src = cv.imread("bug.jpg")

# # Convert image to gray and blur it
# src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# src_gray = cv.blur(src_gray, (3,3))
# source_window = 'Source'
# cv.namedWindow(source_window)
# cv.imshow(source_window, src)
# max_thresh = 300
# thresh = 100 # initial threshold
# cv.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
# thresh_callback(thresh)
# cv.waitKey()


#___________________________
threshold=200 #increasing threshold decreases the contours that are accepted as bounding boxes.


src = cv.imread("fruit.jpg")
# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3,3))

canny_output = cv.Canny(src_gray, threshold, threshold * 2)
contours, hierachy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours_poly = [None]*len(contours)
boundRect = [None]*len(contours)
for i, c in enumerate(contours):
    contours_poly[i] = cv.approxPolyDP(c, 3, True)
    boundRect[i] = cv.boundingRect(contours_poly[i])
print("boundRect: ",boundRect) #format is x, y, w, h where x, y is the coordinate of the top-left of the rectangle
# box0 = boundRect[0] this is the first box in a list of bounding boxes
# coordinates = (box0[0], box0[1], box0[0]+box0[2], box0[1]+box0[3])

