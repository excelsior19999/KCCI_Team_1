import asyncio
import websockets
import cv2
from pathlib import Path
from otx.api.usecases.exportable_code.demo.demo_package import (
    ModelContainer,
    SyncExecutor,
    create_visualizer,
)
# 64, 71

ServerIP = '10.10.14.203'
ServerPort = 6000


async def video_stream():

    # knife-detection model
    model_path = Path('./model')
    model = ModelContainer(model_path, device='CPU')
    visualizer = create_visualizer("sync")
    executor = SyncExecutor(model, visualizer) 

    capture = cv2.VideoCapture(0)   # 동영상 파일 캡처 객체 생성
    # capture = cv2.VideoCapture("/dev/video0")   # 동영상 파일 캡처 객체 생성

    async with websockets.connect(f'ws://{ServerIP}:{ServerPort}') as websocket:
        while capture.isOpened():
            status, frame = capture.read()  # 비디오 프레임 캡처
            if not status:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            predictions, frame_meta = executor.model(frame)
            annotation_scene = executor.converter.convert_to_annotation(predictions, frame_meta)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image = frame
            
            #print(annotation_scene.annotations.scored_label)

            if len(annotation_scene.get_labels()) > 0:
                # probability 값을 추출하는 코드
                for annotation in annotation_scene.annotations:
                    for entity in annotation.get_labels():
                        probability = entity.probability
                        print(f"Probability: {probability}")
                for entity in annotation_scene.shapes:
                    x1, y1 = int(entity.x1 * frame.shape[1]), int(entity.y1 * frame.shape[0])
                    x2, y2 = int(entity.x2 * frame.shape[1]), int(entity.y2 * frame.shape[0])
                    image = cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 255), thickness=2)

            cv2.imshow("image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




            # 이미지 데이터를 문자열로 변환하여 base64로 인코딩
            _, img_buf = cv2.imencode('.jpg', image)
            img_data = img_buf.tobytes()

            # 서버로 스트리밍 데이터 전송
            try:
                await websocket.send(img_data)
            except:
                continue

        # End while
    capture.release()
    cv2.destroyAllWindows()
# End def    

asyncio.get_event_loop().run_until_complete(video_stream())
