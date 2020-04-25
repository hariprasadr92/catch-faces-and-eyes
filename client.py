import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 7090))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(18, 320);
cam.set(12, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    o_data = pickle.dumps(frame, 0)
    o_size = len(o_data)
    print("Size before compression", o_size)
    data = zlib.compress(pickle.dumps(frame, 0))
    #data = pickle.dumps(frame, 0)
    c_size = len(data)
    print("Size after compression", c_size)


    # print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", c_size) + data)
    img_counter += 1

cam.release()