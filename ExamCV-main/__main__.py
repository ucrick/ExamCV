#mengyao liu
import edge
import transform
import text
import verify
import write_results
import numpy as np
import argparse
import cv2
import os
import time
import tkinter as tk
from tkinter import messagebox
from GUI import ExamApp
import preprocess
from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
from skimage.io import imread, imsave
"""
def main():

    cap = cv2.VideoCapture(1)
    root = tk.Tk()
    root.title("Exam App")
    app = ExamApp(root, cap)
    root.mainloop()
    # 在这里访问 rotated_frame
    if app.get_rotated_frame() is not None:
        rotated_frame = app.get_rotated_frame()
        # 进行其他操作
    
    # 检查图像是否成功读取
    if rotated_frame is not None:
        image = rotated_frame
        #image = preprocess.crop_image(image, 1800, 1400)
        print("图像成功读取！")
        orig = image.copy()
    else:
        print("无法读取图像，请检查路径是否正确。")
        
    image = preprocess.adjust_gamma(image)
    image = preprocess.process_image(image)
    orig_image = image
    image = preprocess.combine_process(orig, image)
    #orig_image = image
    
    #边缘检测
    edged,image,ratio = edge.process(image)
    screenCnt, all_rectangles = edge.edge_detection(edged,image)
    
    #透视变换
    transform.transform(orig_image, screenCnt, all_rectangles, ratio)

    #分别读取成绩信息和学生信息
    info_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_info.jpg"
    scr_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_scr.jpg"
    sub_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_sub.jpg"

    #光学识别提取学生信息
    area = "first"
    firstname = text.output_text(info_path, area)
    area = "last"
    lastname = text.output_text(info_path, area)
    area = "id"
    studentid = text.output_text(info_path, area)
    print(firstname,lastname,studentid)
    firstname = firstname.strip()
    lastname = lastname.strip()
    studentid = studentid.strip()

    #光学识别提取成绩信息
    scores = text.output_scr(scr_path)
    print(scores)
    if len(scores) != 0:
        print(scores)
        # 删除文件
        #os.remove("ROI_0")     
    else:
        messagebox.showerror("错误", "未检测到成绩")
    
    # 验证学生信息
    result = verify.find_best_match(firstname, lastname, studentid)

    #验证成绩信息
    is_cor = verify.verify(scores)
    # 将信息写入csv文件中
    if is_cor:
        write_results.output_results(result, scores)
    else:
        messagebox.showerror("错误", "请检查成绩是否正确")
 
        
if __name__ == "__main__":
    main()
    """

def main():
    cap = cv2.VideoCapture(1)
    root = tk.Tk()
    root.title("Exam App")
    app = ExamApp(root, cap)

    # Start the video capture loop
    app.show_video()
    root.mainloop()

if __name__ == "__main__":
    main()