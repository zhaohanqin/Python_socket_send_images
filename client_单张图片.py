import socket
import cv2
import numpy as np
import struct

# 连接服务端
# 创建TCP socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接到本地8010端口
client_socket.connect(('127.0.0.1', 8010))

# 初始化摄像头（当前被注释，使用本地图片代替）
# cap = cv2.VideoCapture(0)
# 读取本地图片文件
frame = cv2.imread("cat.jpg")
# 设置JPEG编码参数（质量等级90%）
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# 图像编码成 JPEG 格式
# 将numpy数组编码为JPEG格式，返回编码结果和图像数据
result, img_encode = cv2.imencode('.jpg', frame, encode_param)
# 将编码后的图像转换为字节数据
data = img_encode.tobytes()

# 发送数据长度（4字节无符号整数）
# 使用网络字节序(!)打包数据长度，I表示unsigned int
client_socket.sendall(struct.pack('!I', len(data)))
# 发送数据
# 解码并打印服务端响应
# 设置接收缓冲区大小为1024字节
client_socket.sendall(data)

# 接收服务端返回信息
reply = client_socket.recv(1024)
print('Server reply:', reply.decode())

# cap.release()
client_socket.close()
