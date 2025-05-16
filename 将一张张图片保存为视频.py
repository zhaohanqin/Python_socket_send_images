import socket
import cv2
import numpy as np
import struct
import os

# 新增：封装视频保存逻辑的类
class VideoSaver:
    """用于管理视频写入的工具类"""
    def __init__(self, video_filename, frame_rate=20):
        self.video_filename = video_filename
        self.frame_rate = frame_rate
        self.video_writer = None  # 视频写入器实例
        self.frame_size = None    # 视频帧尺寸（宽度，高度）

    def write_frame(self, frame):
        """写入单帧图像到视频文件（自动处理首次初始化）"""
        if self.video_writer is None:
            # 首次调用时根据帧尺寸初始化视频写入器
            self.frame_size = (frame.shape[1], frame.shape[0])  # (宽度，高度)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')            # 定义视频编码格式
            self.video_writer = cv2.VideoWriter(
                self.video_filename,
                fourcc,
                self.frame_rate,
                self.frame_size
            )
        self.video_writer.write(frame)  # 写入当前帧

    def release(self):
        """释放视频写入器资源"""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

# 创建保存目录
img_save_dir = 'received_images'
os.makedirs(img_save_dir, exist_ok=True)

# 视频保存参数（修改：使用VideoSaver替代原变量）
video_filename = 'output.avi'
frame_rate = 20  # 可根据实际情况调整
video_saver = VideoSaver(video_filename, frame_rate)  # 初始化视频保存器

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8010))
server_socket.listen(1)
print('Waiting for client...')

conn, adder = server_socket.accept()
print('Client connected from:', adder)

frame_count = 0

while True:
    # 接收数据长度（未修改部分保持原样）
    data_len_bytes = conn.recv(4)
    if not data_len_bytes:
        break
    data_len = struct.unpack('!I', data_len_bytes)[0]

    # 接收图像数据（未修改部分保持原样）
    data = b''
    while len(data) < data_len:
        packet = conn.recv(data_len - len(data))
        if not packet:
            break
        data += packet

    # 解码图像（未修改部分保持原样）
    np_data = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    if img is not None:
        frame_count += 1
        cv2.imshow('Server - Received', img)

        # 保存单帧图片（未修改部分保持原样）
        img_filename = os.path.join(img_save_dir, f'img_{frame_count:04d}.jpg')
        cv2.imwrite(img_filename, img)
        print(f'Saved: {img_filename}')

        # 修改：通过VideoSaver写入视频帧（替代原video_writer.write）
        video_saver.write_frame(img)

        # 发送确认信息（未修改部分保持原样）
        conn.sendall(b'Image received.')

        if cv2.waitKey(1) == 27:
            break
    else:
        print('Failed to decode image.')

# 清理资源（修改：通过VideoSaver释放资源）
conn.close()
server_socket.close()
cv2.destroyAllWindows()
video_saver.release()  # 替代原video_writer.release()
print('Server shutdown, video saved to:', video_filename)