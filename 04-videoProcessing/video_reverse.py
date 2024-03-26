from pathlib import Path

import cv2

DEBUG = False

# cv2.VideoCapture可以读取视频帧 
def getFrames(video_name):
    cap = cv2.VideoCapture(video_name) # 可以是设备名称，也可以是视频文件名称
    check , vid = cap.read()
    if not check:
        print("the video capturing has something wrong.")
        exit()
    frame_list = []
    while(check == True):
        check , vid = cap.read()
        frame_list.append(vid)
    frame_list.pop()
    if DEBUG:
        for frame in frame_list:
            cv2.imshow("Frame" , frame)
            # waitkey method to stopping the frame for some time
            if cv2.waitKey(25) and 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()
    return frame_list


# cv2.VideoWriter可以保存视频帧
# 注意：保存时候的shape和读取时候numpy的shape宽和高是相反的
def revese(video_name):
    stem = Path(video_name).stem
    reverse_path = video_name.replace(stem,'reverse_'+stem)
    frame_list = getFrames(video_name)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # fourcc是用于指定视频编解码器的4字节代码
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(reverse_path,fourcc,30,(frame_list[0].shape[1],frame_list[0].shape[0]),True)
    frame_list.reverse()
    for frame in frame_list:
        print(frame.shape)
        out.write(frame)
        if DEBUG:
            cv2.imshow("reverse Frame" , frame)
            if cv2.waitKey(25) and 0xFF == ord("q"):
                break
        out.write(frame)
    print("finish reverse.")
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    DEBUG=False
    video_name = "bee.mp4"
    revese(video_name)

