import csv
import os
import tkinter as tk

def output_results(result, scores):
    # 检查文件是否存在，如果不存在，则创建文件
    csv_file_path = 'final.csv'
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # 写入表头
            writer.writerow(['firstname', 'lastname', 'studentid', 'score'])
    # 将 scores 列表中的元素转换为整数
    scores = [int(score) for score in scores]
    # 将数据写入CSV文件
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        # 将result和scores数据写入一行
        writer.writerow([result[0], result[1], result[2], scores[-1]])
    
    # 创建主窗口
    root = tk.Tk()
    root.title("student infomation")
    root.geometry("300x150")
    name = "student information:\n" + result[0] + "\n" + result[1] + "\n" + result[2] + "\n" + "scores:\n" + str(scores[-1])
    # 添加学生信息
    label = tk.Label(root, text=name)
    label.pack(pady=20)
    
    # 在5秒后关闭对话框
    root.after(5000, root.destroy)
    
    # 运行主循环
    root.mainloop()
