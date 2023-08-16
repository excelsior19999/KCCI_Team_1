"""
author: 김정균
"""

import socket
import cv2
import pickle
import struct
import os


def run_streaming():
    ServerIP = '10.10.14.3'
    Port = 9876

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 즉시 재사용
    server_socket.bind((ServerIP, Port))
    server_socket.listen(5)
    print(f'LISTENING AT : {ServerIP}:{Port}')

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

                cv2.imshow("RECEIVING VIDEO", frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            # End while

            cv2.destroyAllWindows()
            client_socket.close()

        # End if
    # End while
# End def


def main():
    run_streaming()


    # t1 = threading.Thread(target=def1, args=(,), daemon=True)
    # t2 = threading.Thread(target=def2, args=(,), daemon=True)
    
    # t1.start()
    # print("def1 start")
    # t2.start()
    # print("def2 start")

    # t1.join()
    # t2.join()

# End def


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
