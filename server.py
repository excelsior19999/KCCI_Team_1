"""
author: 김정균
sudo apt install libmariadb-dev
sudo apt install mariadb-server mariadb-client # systemctl status mariadb.service 
sudo apt install mosquitto
"""

import socket
import cv2
import pickle
import struct
import os
import sys
import threading
import mariadb
import json
from queue import Queue


ServerIP = '10.10.14.3'
Event = False


def run_streaming(Port, msg_queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 즉시 재사용
    server_socket.bind((ServerIP, Port))
    server_socket.listen(5)
    print(f'\nStreaming(Filed Client) LISTENING AT : {ServerIP}:{Port}')

    data = b""
    payload_size = struct.calcsize("Q")  # 8byte

    while True:
        print('waiting accept...')
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        if client_socket:
            while True:

                # 직렬화된 data(frame 1개 담을 변수) revc
                if len(data) < payload_size:  # 한 frame 시작 부분이면 4kb만 받기(길이 알기 위함)
                    packet = client_socket.recv(4*1024)  # 4096byte(4kb) packet recv
                    if not packet:
                        break
                    data += packet  # 한 frame 읽을 때까지 반복
                # End while

                if len(data) == 0:
                    break

                # msg_size 추출
                packed_msg_size = data[:payload_size]  # msg 크기를 나타내는 data 추출
                data = data[payload_size:]  # msg 내 길이 정보 제거
                msg_size = struct.unpack("Q", packed_msg_size)[0]  # 역직렬화하여 실제 msg len 정보 추출

                # 나머지 msg까지 완전히 수신
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                # End while
                
                frame_data = data[:msg_size]  # 길이 정보 제거한 data 부분
                data = data[msg_size:]  # data 초기화
                frame = pickle.loads(frame_data)  # 역직렬화(byte sequence를 frame 객체로 변환)
                
                if Event == True:
                    # 동영상 저장 설정
                    from datetime import datetime
                    now = datetime.now()

                    output_filename = f'{now.date()}_{now.time()}.mp4'  # 저장할 동영상 파일 이름
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정 (XVID는 AVI 형식)
                    fps = 30.0  # 초당 프레임 수
                    frame_size = (640, 480)  # 프레임 크기

                    # VideoWriter 객체 생성
                    out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)
                    
                    # 프레임 저장
                    out.write(frame)
                    
                    # 화면에 프레임 출력
                    # cv2.imshow('Video Recording', frame)

                    # 리소스 해제
                    out.release()
                    # cv2.destroyAllWindows()
                # End if


                # 직렬화된 frame data => frame_data
                serialFrame = frame_data
                message = struct.pack("Q", len(serialFrame)) + serialFrame  # 직렬화된 frame의 길이(Q==8) + 직렬화된 data => recv할때 해당 길이만큼 데이터 역직렬화
                msg_queue.put(message)
                # client_socket.sendall(message)  # frame(한 장) byte로 전송

                # cv2.imshow("RECEIVING VIDEO", frame)
                # if cv2.waitKey(10) & 0xFF == ord('q'):
                #     break
            # End while

            # cv2.destroyAllWindows()
            client_socket.close()

        # End if
    # End while
# End def


def run_mqtt():
    os.system('mosquitto -p 1888')
# End def    


def send_streaming(Port, msg_queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 즉시 재사용
    server_socket.bind((ServerIP, Port))
    server_socket.listen(5)
    print(f'\nStreaming(QTClient) LISTENING AT : {ServerIP}:{Port}')

    while True:
        print('waiting accept...')
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        if client_socket:

            # serialize frame 그대로 전송
            while True:
                try:
                    serialFrame = msg_queue.get_nowait()
                except:
                    continue
                client_socket.sendall(serialFrame)  # frame(한 장) byte로 전송

            client_socket.close()
        # End if
    # End while
# End def    


# DB
def client_db_req(Port, cur):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 즉시 재사용
    server_socket.bind((ServerIP, Port))
    server_socket.listen(5)
    print(f'\nDB Request LISTENING AT : {ServerIP}:{Port}')

    while True:
        print('waiting accept...')
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        if client_socket:
            cur.execute(
                "SELECT * \
                   FROM TB_DDUKNIP \
                  WHERE MACHINE_NAME=? \
                  ORDER BY EVENT_DATE DESC \
                  LIMIT 1"
                , ('TurtleBot',)
            )
            
            # Print Result-set
            for (VIDEO_NAME, GPS_COORDINATE) in cur:
                print(f"VIDEO_NAME: {VIDEO_NAME}, GPS_COORDINATE: {GPS_COORDINATE}")


            client_socket.send(cur.encode('utf-8'))
        # End if


            #client_socket.close()
        # End if
    # End while
# End def   


def recv_from_field(Port, cur, conn):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 즉시 재사용
    server_socket.bind((ServerIP, Port))
    server_socket.listen(5)
    print(f'\nrecv_from_field LISTENING AT : {ServerIP}:{Port}')

    while True:
        print('waiting accept...')
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        if client_socket:
            while True:

                recvData = client_socket.recv(1024).decode('utf-8')
                if not recvData:
                    break
                print(f"수신한 데이터: {type(recvData)}")

                dictData = json.loads(recvData)
                print(dictData)

                global Event
                if dictData['event_yn'] == True:
                    # 영상 저장
                    Event = True
                else:
                    Event = False


                # INSERT
                try: 
                    cur.execute("INSERT INTO TB_DDUKNIP ( \
                                    MACHINE_NAME \
                                    VIDEO_NAME \
                                    GPS_COORDINATE \
                                    EVENT_YN \
                                ) VALUES \
                                    (?, ?, ?, ?, ?)"
                                , 
                                ("TurtleBot"
                                 , path
                                 , dictData['gps']
                                 , dictData['event_yn']
                                 )) 
                except mariadb.Error as e: 
                    print(f"Error: {e}")

                conn.commit() 
                print(f"Last Inserted ID: {cur.lastrowid}")


            # End while
        # End if
    # End while
# End def


def main():
    # run_streaming()
    # client_req()

    msg_queue = Queue()

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="user1",
            password="user1",
            host="127.0.0.1",
            port=3306,
            database="TB_DDUKNIP"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    run_mqtt()
    t1 = threading.Thread(target=run_streaming, args=(9876, msg_queue, ), daemon=True)
    t2 = threading.Thread(target=send_streaming, args=(9888, msg_queue, ), daemon=True)
    t3 = threading.Thread(target=client_db_req, args=(9899, cur), daemon=True)
    t4 = threading.Thread(target=recv_from_field, args=(9777, cur, conn), daemon=True)  # GPS, 상황발생YN 받기
    
    t1.start()
    print("run_streaming start")
    t2.start()
    print("send_streaming start")
    t3.start()
    print("client_db_req start")
    t4.start()
    print("recv_from_field start")

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    conn.close()
# End def


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
