from PIL import Image, ImageTk
#mengyao liu
import edge
import edge_info
import edge_scr
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
import preprocess
from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
from skimage.io import imread, imsave
"""
class ExamApp:
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap

        self.video_label = tk.Label(root)
        self.video_label.pack(padx=10, pady=10)

        self.screenshot_button = tk.Button(root, text="screenshot", command=self.capture_screenshot)
        self.screenshot_button.pack(pady=5)

        self.rotate_button = tk.Button(root, text="rotate", command=self.rotate_image)
        self.rotate_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="exit", command=self.quit_app)
        self.quit_button.pack(pady=5)

        self.show_video()

    def show_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            self.root.after(10, self.show_video)
        else:
            self.root.destroy()

    def capture_screenshot(self):
        ret, frame = self.cap.read()
        if ret:
            self.rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.rotated_frame = cv2.cvtColor(self.rotated_frame, cv2.COLOR_BGR2RGB)            
            cv2.imwrite('screenshot.png', self.rotated_frame)
            print('截图已保存')

    def rotate_image(self):
        ret, frame = self.cap.read()
        if ret:
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rotated_frame)
            photo = ImageTk.PhotoImage(image=image)
            rotated_window = tk.Toplevel(self.root)
            rotated_label = tk.Label(rotated_window, image=photo)
            rotated_label.photo = photo
            rotated_label.pack()
            
    def get_rotated_frame(self):
        return self.rotated_frame        

    def quit_app(self):
        self.cap.release()
        self.root.destroy()

"""


class ExamApp:
    def __init__(self, root, cap):
        self.root = root
        self.cap = cap
        self.rotated_frame = None

        self.video_label = tk.Label(root)
        self.video_label.pack(padx=10, pady=10)

        self.screenshot_button = tk.Button(root, text="screenshot", command=self.capture_screenshot)
        self.screenshot_button.pack(pady=5)

        self.rotate_button = tk.Button(root, text="rotate", command=self.rotate_image)
        self.rotate_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="exit", command=self.quit_app)
        self.quit_button.pack(pady=5)

        self.show_video()

    def show_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            self.root.after(10, self.show_video)
        else:
            self.root.destroy()

    def capture_screenshot(self):
        ret, frame = self.cap.read()
        if ret:
            self.rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.rotated_frame = cv2.cvtColor(self.rotated_frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite('screenshot.png', self.rotated_frame)
            # Call a method to process the captured image
            self.root.after(100, self.process_captured_image)

    def rotate_image(self):
        ret, frame = self.cap.read()
        if ret:
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rotated_frame)
            photo = ImageTk.PhotoImage(image=image)
            rotated_window = tk.Toplevel(self.root)
            rotated_label = tk.Label(rotated_window, image=photo)
            rotated_label.photo = photo
            rotated_label.pack()

    def get_rotated_frame(self):
        return self.rotated_frame

    def process_captured_image(self):

        image = self.rotated_frame
        orig_image = image
        edged, image, ratio = edge.process(image)
        screenCnt, all_rectangles = edge.edge_detection(edged, image) 
        image = transform.transform(orig_image, screenCnt, all_rectangles, ratio)
        #image = cv2.imread("scan_papper.jpg")
        orig = image.copy() 
        #image = preprocess.adjust_gamma(all_rectangles[0])
        image_1 = preprocess.process_image(image)
        image_2 = preprocess.combine_process(orig, image_1)
        # 获取图像的宽度和高度
        height, width = image_1.shape
        center_x = width // 2
        center_y = height // 2        
        cropped_info = image_1[center_y+height//7:center_y+height//2, center_x-width//2:center_x+width//6]
        cropped_scr = image_1[center_y:center_y+height//2, center_x+width//5:center_x+width//2]
        info_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_info.jpg"
        scr_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_scr.jpg"
        #sub_path = "C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_sub.jpg"
        #image_scr = cv2.imread(scr_path)  

        image_info = edge_info.save_image(cropped_info)
        image_scr = edge_scr.save_image(cropped_scr)
        #cv2.imwrite("scan_scr.jpg", image_scr)
        #edged, image_scr, ratio = edge.process(cropped_scr)
        #screenCnt, all_rectangles = edge.edge_detection(edged, image_scr)
        #cv2.imwrite("scan_scr2.jpg", all_rectangles[0].reshape(4, 2) * ratio)
        area = "first"
        firstname = text.output_text(image_info, area)
        area = "last"
        lastname = text.output_text(image_info, area)
        area = "id"
        studentid = text.output_text(image_info, area)
        print(firstname, lastname, studentid)
        firstname = firstname.strip()
        lastname = lastname.strip()
        studentid = studentid.strip()
        #firstname = "williams"
        #lastname = "james"
        #studentid = "12345678"
        #scores = [10,9,8,13,40]
        scores = text.output_scr(image_scr)
        print(scores)

        if len(scores) != 0:
            print(scores)
        else:
            messagebox.showerror("error", "No grades detected")

        result = verify.find_best_match(firstname, lastname, studentid)
        is_cor = verify.verify(scores)

        if is_cor:
            write_results.output_results(result, scores)
        else:
            messagebox.showerror("error", "Please check if the grades are correct")

    def quit_app(self):
        self.cap.release()
        self.root.destroy()
