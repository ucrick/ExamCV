import cv2
from imutils import contours
import resize
import numpy as np
import pytesseract
from tkinter import messagebox
from PIL import Image, ImageEnhance

scores = []

NAMES_CONFIG = r'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
ID_CONFIG = r'--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789'


def output_text(image, area):

    # 确定手写数字的区域
    #image = cv2.imread(path)
    #height, width, _ = image.shape
    #one_third_x = width // 3
    #one_eighth_x = width // 8
    #one_sixth_y = height // 6
    #one_third_y = height // 3      
    if area == "first":
        #x_start, x_end, y_start, y_end = one_third_x-5, width - one_eighth_x, 15, one_third_y
        x_start, x_end, y_start, y_end = 78, 220, 4, 35
        custom_config = NAMES_CONFIG
    elif area == "last":
        #x_start, x_end, y_start, y_end = one_third_x-5, width - one_eighth_x, one_third_y, one_third_y+one_sixth_y
        x_start, x_end, y_start, y_end = 78, 220, 31, 65
        custom_config = NAMES_CONFIG
    elif area == "id":
        #x_start, x_end, y_start, y_end = one_third_x-5, width - one_eighth_x, one_third_y+one_sixth_y, one_third_y+2*one_sixth_y
        x_start, x_end, y_start, y_end = 78, 220, 64, 87
        custom_config = ID_CONFIG
    else:
        print("error")    
    
    # 裁剪图像
    cropped_image = image[y_start:y_end, x_start:x_end]

    #kernel = np.ones((3, 1), dtype=np.uint8)
    #row = cv2.erode(cropped_image, kernel, iterations = 1)
    
    
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    
    if cropped_image is None or cropped_image.size == 0:
        messagebox.showerror("error", "No student information detected")
        return "error"
    else:
        # 中值滤波平滑
        #smoothed = cv2.medianBlur(cropped_image, 3)       
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        #cleaned_image = cv2.morphologyEx(smoothed, cv2.MORPH_OPEN, kernel, iterations=1)    
        cv2.imshow("shibie", cropped_image)
        cv2.waitKey(0)
        
        # 进行 OCR 识别
        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        
        return text        
"""
def output_scr(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x_start, x_end, y_start = 46, 87, 55
    cropped_image = image[y_start:, x_start:x_end]   
    
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 每行间距和横线宽度
    line_spacing = 35
    line_width = 2
    
    # 分割图像
    rows = []
    start_row = 0
    end_row = line_spacing
    
    while end_row < cropped_image.shape[0]:
        row_subset = cropped_image[start_row:end_row, :]
        rows.append(row_subset)
        start_row = end_row + line_width
        end_row = start_row + line_spacing
    
    # 识别每个子集
    for i, row in enumerate(rows, start=1):
        row = cv2.resize(row, (256, 256))
        
        #kernel = np.ones((5, 5), dtype=np.uint8)
        #fin = cv2.dilate(row, kernel, iterations=2)
        
        # 应用卷积核
        #fin = cv2.resize(row, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)      
        

        # 显示每个子集的图片
        cv2.imshow(f"Row {i}", fin)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 中值滤波平滑
        thresh = cv2.medianBlur(row, 9) 
        #thresh = cv2.GaussianBlur(row, (9, 9), 0)
        #thresh = cv2.blur(row, (5, 5))
        #thresh = cv2.adaptiveThreshold(row, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 31, 2) 
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        #thresh = cv2.morphologyEx(row, cv2.MORPH_OPEN, kernel, iterations=2) 
        #thresh = cv2.bilateralFilter(row, 9, 75, 75)     
        cv2.imshow("Image", thresh)
        cv2.waitKey(0)        
        
        numbers_in_row = pytesseract.image_to_string(thresh, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        
        cleaned_string = numbers_in_row.strip()  # 去掉字符串两端的空格

        if cleaned_string:  # 如果字符串不为空
            try:
                result_integer = int(cleaned_string)
                # 在这里可以使用 result_integer
                scores.append(result_integer)
            except ValueError:
                scores.append(0)
        else:
            scores.append(0)
        
    return scores
"""
        
def output_scr(image):
    #image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)   
    x_start, y_start = 33,36
    cropped_image = image[y_start:, x_start:]
    cv2.imshow("shibie", cropped_image)
    cv2.waitKey(0)    
    original = cropped_image
    canny = cv2.Canny(cropped_image, 10, 20) 
    if canny is None:
        print("图片为空")
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2)) 
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    erode = cv2.erode(canny, vertical_kernel)
    dilate = cv2.dilate(erode, kernel, iterations=2)  
    cv2.imshow("Image", dilate)
    cv2.waitKey(0)    
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    digit_contours = []
    for c in cnts:
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        
        if (aspect_ratio >= 0.1 and aspect_ratio <= 1.5):
            if area > 100:
                ROI = original[y:y+h, x:x+w]
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                digit_contours.append(c)
    try:
        sorted_digit_contours = contours.sort_contours(digit_contours, method='top-to-bottom')[0]
    except ValueError as e:
        messagebox.showerror("error", "Please check if the grades are correct")
     
    contour_number = 0
    for c in sorted_digit_contours:           
        x,y,w,h = cv2.boundingRect(c)
        ROI = original[y:y+h, x:x+w]
        numbers_in_row = pytesseract.image_to_string(ROI, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
        cleaned_string = numbers_in_row.strip()
        print(cleaned_string)
        if cleaned_string:  # 如果字符串不为空
            try:
                result_integer = int(cleaned_string)
                # 在这里可以使用 result_integer
                scores.append(result_integer)
            except ValueError:
                scores.append(0)
        else:
            scores.append(0)        
        cv2.imwrite('ROI_{}.png'.format(contour_number), ROI)
        contour_number += 1
        
    return scores

def output_sub(path):
    image = cv2.imread(path)
    # 去掉噪音点
    #gray = cv2.GaussianBlur(image, (3, 3), 0)
    
    # 中值滤波平滑
    #smoothed = cv2.medianBlur(image, 5)
    cv2.imshow("Scanned3", image)
    cv2.waitKey(0)  # 等待按键事件，避免循环等待
    cv2.destroyAllWindows()    
    text = pytesseract.image_to_string(image, config = r'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    return text    