import os
import sys
import cv2
from pathlib import Path

from otx.api.usecases.exportable_code.demo.demo_package import (
    ModelContainer,
    SyncExecutor,
    create_visualizer,
)

def main():

    model_path = Path('/home/intel/workspace/knife-detection/outputs/20230821_160548_deploy/model')
    model = ModelContainer(model_path, device='CPU')
    visualizer = create_visualizer("sync")
    executor = SyncExecutor(model, visualizer) 

    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        status, frame = capture.read()  
        if not status:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predictions, frame_meta = executor.model(frame)
        annotation_scene = executor.converter.convert_to_annotation(predictions, frame_meta)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image=frame
        
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

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(main() or 0)