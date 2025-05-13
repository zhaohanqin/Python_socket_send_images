import socket
import cv2
import numpy as np
import struct
import os

# 创建保存目录
img_save_dir = 'received_images'
os.makedirs(img_save_dir, exist_ok=True)

# 视频保存参数
video_filename = 'output.avi'
video_writer = None
frame_size = None
frame_rate = 20  # 可根据实际情况调整

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8010))
server_socket.listen(1)
print('Waiting for client...')

conn, adder = server_socket.accept()
print('Client connected from:', adder)

frame_count = 0

while True:
    # 接收数据长度
    data_len_bytes = conn.recv(4)
    if not data_len_bytes:
        break
    data_len = struct.unpack('!I', data_len_bytes)[0]

    # 接收图像数据
    data = b''
    # 持续接收数据包直到接收完整
    while len(data) < data_len:
        packet = conn.recv(data_len - len(data))
        if not packet:  # 连接中断时退出循环
            break
        data += packet  # 拼接数据包

    # 将字节数据转换为OpenCV图像格式
    # 将接收到的字节数据转换为NumPy数组，数据类型为无符号8位整数
    np_data = np.frombuffer(data, dtype=np.uint8)

    # 使用OpenCV解码JPEG格式的图像数据，将其转换为图像矩阵
    # cv2.IMREAD_COLOR 表示以彩色模式加载图像
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    if img is not None:  # 图像解码成功
        frame_count += 1  # 帧计数器递增
        cv2.imshow('Server - Received', img)  # 显示实时画面

        # 视频写入器延迟初始化（等待第一帧到达后获取尺寸）
        if video_writer is None:
            # 获取图像尺寸（宽度在前，高度在后）
            # OpenCV的shape返回格式为（高度，宽度，通道数），这里取[1]宽度，[0]高度
            frame_size = (img.shape[1], img.shape[0])

            # 创建XVID编码的视频写入器
            # FourCC是四字符编码的编解码器标识，XVID是MPEG-4视频编码格式，具有较好的压缩率
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 解包字符串为四个字符参数

            # 初始化视频写入器参数：
            # video_filename: 输出文件名
            # fourcc: 视频编解码器
            # frame_rate: 帧率（单位：FPS）
            # frame_size: 视频分辨率（宽度，高度）
            video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, frame_size)

        # 保存单帧图片到指定目录（格式：img_0001.jpg）
        img_filename = os.path.join(img_save_dir, f'img_{frame_count:04d}.jpg')
        cv2.imwrite(img_filename, img)
        print(f'Saved: {img_filename}')

        # 将当前帧写入视频文件
        video_writer.write(img)

        # 发送接收确认信息给客户端
        conn.sendall(b'Image received.')

        if cv2.waitKey(1) == 27:  # 按下ESC键退出循环
            break
    else:
        print('Failed to decode image.')

# 清理资源
conn.close()
server_socket.close()
cv2.destroyAllWindows()
if video_writer:
    video_writer.release()
print('Server shutdown, video saved to:', video_filename)
