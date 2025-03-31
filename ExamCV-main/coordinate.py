import cv2

# 定义鼠标回调函数
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"点击坐标：({x}, {y})")

image = cv2.imread("C:\\Users\\User\\Documents\\GitHub\\ExamCV\\scan_scr.jpg")

# 创建窗口并设置鼠标回调函数
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", on_mouse_click)

# 显示图像
cv2.imshow("Image", image)

# 等待键盘输入，按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()

