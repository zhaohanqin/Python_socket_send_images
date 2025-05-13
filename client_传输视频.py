import socket
import cv2
import numpy as np
import struct

# 连接服务端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8010))

cap = cv2.VideoCapture("2.mp4")

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 图像编码成 JPEG 格式
    result, img_encode = cv2.imencode('.jpg', frame, encode_param)
    data = img_encode.tobytes()

    # 发送数据长度（4字节无符号整数）
    client_socket.sendall(struct.pack('!I', len(data)))
    # 发送数据
    client_socket.sendall(data)

    # 接收服务端返回信息
    reply = client_socket.recv(1024)
    print('Server reply:', reply.decode())

    if cv2.waitKey(1) == 27:
        break

cap.release()
client_socket.close()
