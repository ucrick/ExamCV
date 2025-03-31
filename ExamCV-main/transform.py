import resize
import numpy as np
import argparse
import cv2
import os


def order_points(pts):
    #一共4个坐标点
    rect = np.zeros((4,2),dtype="float32")
    
    #按照顺序找到对应坐标0123分别是左上，右上右下左下
    #计算左上，右下
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    #计算右上和左下
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    #获取输入坐标点
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    #计算输入的w和h值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    #变换后对应的坐标值
    dst = np.array([
        [0,0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    
    #计算变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
  
    #返回结果
    return warped

def transform(orig, screenCnt, all_rectangles, ratio):
    #信息透视变换
    warped = four_point_transform(orig, all_rectangles[0].reshape(4, 2) * ratio)

    cv2.imshow("resize", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #cv2.imwrite("scan_papper.jpg", warped)
    
    #展示结果
    print("第三步：变换")
    return warped

