import cv2
import numpy as np
from propainter import Propainter

# 初始化视频捕捉
video_path = 'F:/Users/98/Documents/1111.avi'
cap = cv2.VideoCapture(video_path)

# 创建一个 Propainter 对象
propainter = Propainter()

# 定义要去除的区域（例如，左上角的矩形区域）
x1, y1, x2, y2 = 100, 100, 300, 300  # 根据需要调整坐标

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 创建掩码，指定区域为白色，其余区域为黑色
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255  # 将指定区域设为白色

    # 使用 Propainter 去除指定区域
    result_frame = propainter.remove(frame, mask)

    # 显示结果
    cv2.imshow('Original', frame)
    cv2.imshow('Processed', result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
