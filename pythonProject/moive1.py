import cv2
import numpy as np

# 读取视频
cap = cv2.VideoCapture('F:/Users/98/Documents/IMG_8663.MOV')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('F:/Users/98/Documents/1111.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

# 定义要消除的区域坐标
x1, y1, x2, y2 = 100, 50, 400, 150  # 替换为你的坐标

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 创建掩膜
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255  # 设置要消除的区域

    # 使用 inpaint 方法修复区域
    result = cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    # 写入输出视频
    out.write(result)

cap.release()
out.release()
cv2.destroyAllWindows()
