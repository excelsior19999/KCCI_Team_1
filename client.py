"""
author: 김정균
sudo apt install mosquitto
"""

import socket
import cv2
import pickle
import struct
import os
import paho.mqtt.client as mqtt
import threading
from time import sleep


ServerIP = '10.10.14.3'
resData = -1


def run_streaming():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ServerIP, 9876))
    
    ### Start cv
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("/home/intel/repo/kcci.intel.ai.project/Class02/smart_factory_src/resources/factory/conveyor.mp4")
    # fcnt = 0
    while True:
        _, frame = cap.read()
        if frame is None:
            break

        serialFrame = pickle.dumps(frame)  # 직렬화(byte sequence로 변환)
        message = struct.pack("Q", len(serialFrame)) + serialFrame  # 직렬화된 frame의 길이(Q==8) + 직렬화된 data => recv할때 해당 길이만큼 데이터 역직렬화
        client_socket.sendall(message)  # frame(한 장) byte로 전송

        cv2.imshow('TRANSMITTING VIDEO', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        # fcnt += 1
        # print(f'{fcnt}. len(message) : {len(message)}')
    # End while

    client_socket.close()
    cv2.destroyAllWindows()
    cap.release()
    ### End cv
    
# End def


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# End def


# subscriber callback
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic= ", message.topic)
    print("message qos=", message.qos)
    print("message retain flag= ", message.retain)

    global resData
    resData = str(message.payload.decode("utf-8"))

    print(f'mqtt mag : {resData}')
# End def


def mqtt_sub():
    mqtt_sub = mqtt.Client('field_client')
    mqtt_sub.on_connect = on_connect
    mqtt_sub.on_message = on_message
    mqtt_sub.subscribe('vigilante/action')
    # try:
    mqtt_sub.connect(ServerIP, 1888)
    # except Exception as e:
        # print(f'except@@@@@@@@@@@@@@@@@@@@@ : {e}') # [Errno 111] Connection refused
    
    print('wait mqtt msg')
    mqtt_sub.loop_forever()
# End def


def main():
    # run_streaming()
    # mqtt_sub()

    t1 = threading.Thread(target=run_streaming, args=(), daemon=True)
    t2 = threading.Thread(target=mqtt_sub, args=(), daemon=True)
    
    t1.start()
    print("run_streaming start")
    t2.start()
    print("mqtt_sub start")

    t1.join()
    t2.join()

    
# End def    


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
