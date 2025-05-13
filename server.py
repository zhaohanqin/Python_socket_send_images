import socket
import cv2
import numpy as np
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8010))
server_socket.listen(1)
print('Waiting for client...')

conn, addr = server_socket.accept()
print('Client connected from:', addr)

while True:
    # 接收数据长度
    data_len_bytes = conn.recv(4)
    if not data_len_bytes:
        break
    data_len = struct.unpack('!I', data_len_bytes)[0]

    # 接收图像数据
    data = b''
    while len(data) < data_len:
        packet = conn.recv(data_len - len(data))
        if not packet:
            break
        data += packet

    # 解码并显示图像
    np_data = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (1080, 720))
    if img is not None:
        cv2.imshow('Server - Received', img)
        if cv2.waitKey(1) == 27:
            break
        conn.sendall(b'Image received.')
    else:
        print('Failed to decode image.')

conn.close()
server_socket.close()
cv2.destroyAllWindows()
