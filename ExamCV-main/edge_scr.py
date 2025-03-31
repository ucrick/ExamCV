import resize
import numpy as np
import argparse
import cv2
import os

all_rectangles = []

def process(image):
    # 坐标也会相同变化
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = resize.my_resize(orig, height=500)
    # 检测边缘
    edged = cv2.Canny(image, 50, 100)
    # 展示与处理结果
    print("第一步，边缘检测")
    
    return edged, image, ratio

def edge_detection(edged, image):
    # 轮廓检测
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    some_threshold = 200  # 这里使用一个具体的阈值，你可以根据需要调整
    
    # 确保找到了轮廓
    if len(contours) > 0:
        # 过滤掉太小的轮廓
        valid_contours = [cnt.astype('float32') for cnt in contours if len(cnt) >= 3 and cv2.contourArea(cnt.astype('float32')) > some_threshold]
        print(len(valid_contours))
        # 确保找到了有效轮廓
        if len(valid_contours) > 0 :
            # 对有效轮廓按照面积降序排序
            cnts = sorted(valid_contours, key=cv2.contourArea, reverse=True)[:]           
        elif len(valid_contours) == 0:
            print("未找到有效的轮廓。")
    else:
        print("未找到轮廓。")
    
    # 遍历轮廓
    for c in cnts:
        # 计算轮廓近似值
        peri = cv2.arcLength(c, True)
        # 将连续的点近似看成矩形
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)  # 适用于水平矩形
        # 4个点是矩形
        if len(approx) == 4:
            screenCnt = approx
            screenCnt = screenCnt.reshape(-1, 2).astype(int)  # 转换为整数类型
            all_rectangles.append(screenCnt)
            # cv2.polylines(image, [screenCnt], isClosed=True, color=(0,255,0), thickness=2)
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)  # 注意这里将 screenCnt 套在列表中
            # 显示包含轮廓的图像

    # 检查是否找到符合条件的轮廓
    if screenCnt is not None and len(screenCnt) > 0:
        # 展示结果
        print("第二部：获取轮廓")
    else:
        print("未找到符合条件的轮廓。")
    
    return screenCnt, all_rectangles

"""
def save_image(image):
    orig = image
    edged, image, ratio = process(image)
    screenCnt, all_rectangles = edge_detection(edged, image)
    x, y, w, h = cv2.boundingRect(all_rectangles[0].reshape(4, 2).astype(int))
    result = orig[int(y*ratio):int((y+h)*ratio), int(x*ratio):int((x+w)*ratio)]
    cv2.imshow("result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    """
def save_image(image):
    orig = image
    edged, image, ratio = process(image)
    screenCnt, all_rectangles = edge_detection(edged, image)
    
    # 寻找面积最大的轮廓
    max_contour = max(all_rectangles, key=cv2.contourArea)
    
    # 在图像上绘制最大轮廓
    cv2.drawContours(image, [max_contour], -1, (0, 255, 0), 2)
    
    # 获取包围最大轮廓的矩形坐标
    x, y, w, h = cv2.boundingRect(max_contour.reshape(4, 2).astype(int))
    
    # 裁剪并显示结果
    result = orig[int(y * ratio):int((y + h) * ratio), int(x * ratio):int((x + w) * ratio)]
    cv2.imshow("Result with Max Contour", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result
