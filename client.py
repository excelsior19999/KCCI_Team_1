"""
author: 김정균
"""

import socket
import cv2
import pickle
import struct
import os
import paho.mqtt.client as mqtt
import threading
import json
from queue import Queue
from time import sleep


ServerIP = '192.168.100.75'
resData = -1


def run_streaming(Port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ServerIP, Port))

    try:    
        cap = cv2.VideoCapture("/dev/video0")
        #cap = cv2.VideoCapture("/home/intel/repo/kcci.intel.ai.project/Class02/smart_factory_src/resources/factory/conveyor.mp4")
        while True:
            _, frame = cap.read()
            if frame is None:
                break

            serialFrame = pickle.dumps(frame)  # 직렬화(byte sequence로 변환)
            message = struct.pack("Q", len(serialFrame)) + serialFrame  # 직렬화된 frame의 길이(Q==8) + 직렬화된 data => recv할때 해당 길이만큼 데이터 역직렬화
            try:
                client_socket.sendall(message)  # frame(한 장) byte로 전송
            except: # ConnectionResetError:
                continue

            # cv2.imshow('TRANSMITTING VIDEO', frame)
            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #     break
        # End while
    except KeyboardInterrupt:
        print("Client shutting down...")
        client_socket.close()
        cap.release()

    # cv2.destroyAllWindows()
    client_socket.close()
    cap.release()
    
# End def


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))  # 0이면 정상 연결

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

    ### TODO
    ### 메시지에 따른 대응

# End def


def mqtt_sub():
    mqtt_sub = mqtt.Client('field_client')
    mqtt_sub.on_connect = on_connect
    mqtt_sub.on_message = on_message
    mqtt_sub.subscribe('vigilante/action')
    try:
        mqtt_sub.connect(ServerIP, 1888)
    except:
        print('mqtt connect error')
    
    print('wait mqtt msg')
    mqtt_sub.loop_forever()
# End def


def info_send(Port, msg_queue):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ServerIP, Port))
    req_data = dict()

    while True:
        # TODO : GPS 모듈로 값 받기

        gps = '37.5413, 126.841'  # KFC
        try:
            event_yn = msg_queue.get_nowait()  # from  def ai_func(msg_queue):
        except:
            continue

        req_data['gps'] = gps
        req_data['event_yn'] = event_yn

        sleep(1)
        client_socket.socket.send(json.dumps(req_data).encode('UTF-8'))
    # End while

    client_socket.close()
# End def


def ai_func(msg_queue):
    while True:
        ### TODO
        ### 사건 발생 유무 받아서 event_yn에 넣기
        event_yn = False
        msg_queue.put(event_yn)
    # End while
# End def    


def main():
    # run_streaming()
    # mqtt_sub()

    msg_queue = Queue()

    t1 = threading.Thread(target=run_streaming, args=(9876, ), daemon=True)
    t2 = threading.Thread(target=mqtt_sub, args=(), daemon=True)
    t3 = threading.Thread(target=info_send, args=(9777, msg_queue), daemon=True)
    # t_ai = threading.Thread(target=ai_func, args=(msg_queue, ), daemon=True)
    
    t1.start()
    print("run_streaming start")
    t2.start()
    print("mqtt_sub start")
    t3.start()
    print("info_send start")
    # t_ai.start()
    # print("t_ai start")

    t1.join()
    t2.join()
    t3.join()
    # t_ai.join()

    
# End def    


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
