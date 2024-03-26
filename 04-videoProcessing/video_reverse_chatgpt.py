import cv2

# 打开视频文件
cap = cv2.VideoCapture('bee.mp4')

# 获取视频的帧率和尺寸
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 存储帧的列表
frames = []

# 读取视频的每一帧并存储到列表中
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    print(frame.shape)
    frames.append(frame)

# 关闭视频文件
cap.release()

# 创建一个新的视频文件
print(width,height)
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# 将存储帧的列表进行逆序处理，并将每一帧写入新的视频文件中
for frame in reversed(frames):
    out.write(frame)

# 关闭视频文件
out.release()
