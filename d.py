from multiprocessing import Process, Queue
import cv2
from ultralytics import YOLO
import numpy as np
import time

def in_function(name, file_index):
    cap = cv2.VideoCapture(0)

    coco_model = YOLO('model/yolov8n.pt')
    license_plate_model = YOLO('model/license_plate.pt')

    while True:
        ret, frame = cap.read()  # Read the video frames

        # Exit the loop if no more frames in either video
        if not ret:
            break

        left_rect = (0, 0, int(frame.shape[1] / 2), frame.shape[0])
        cv2.rectangle(frame, left_rect[:2], left_rect[2:], (0, 255, 0), 2)
        color = (0, 255, 0)
        left_text = "Entrada"

        left_text_pos = (left_rect[0] + (left_rect[2] - left_rect[0]) // 2 - 50, left_rect[1] + 20)
        cv2.putText(frame, left_text, left_text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        area_pts_left = np.array([[left_rect[0], left_rect[1]], [left_rect[0], left_rect[3]],
                                  [left_rect[2], left_rect[3]], [left_rect[2], left_rect[1]]])
        cv2.drawContours(frame, [area_pts_left], -1, (0, 255, 0), 2)
        in_frame = np.zeros(frame.shape, dtype=np.uint8)
        in_frame = cv2.drawContours(in_frame, [area_pts_left], -1, (255, 255, 255), -1)
        in_frame = cv2.bitwise_and(frame, in_frame)

        in_frame = frame[:, :frame.shape[1] // 2]

        cv2.imshow(name, in_frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            exit()


def out_function(name, file_index):
    cap = cv2.VideoCapture(0)

    coco_model = YOLO('model/yolov8n.pt')
    license_plate_model = YOLO('model/license_plate.pt')

    while True:
        ret, frame = cap.read()  # Read the video frames

        # Exit the loop if no more frames in either video
        if not ret:
            break

        right_rect = (int(frame.shape[1] / 2), 0, frame.shape[1], frame.shape[0])
        cv2.rectangle(frame, right_rect[:2], right_rect[2:], (0, 255, 0), 2)
        color = (0, 255, 0)
        right_text = "Salidas"

        right_text_pos = (right_rect[0] + (right_rect[2] - right_rect[0]) // 2 - 50, right_rect[1] + 20)
        cv2.putText(frame, right_text, right_text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        area_pts_right = np.array([[right_rect[0], right_rect[1]], [right_rect[0], right_rect[3]],
                                   [right_rect[2], right_rect[3]], [right_rect[2], right_rect[1]]])
        cv2.drawContours(frame, [area_pts_right], -1, (0, 255, 0), 2)
        out_frame = np.zeros(frame.shape, dtype=np.uint8)
        out_frame = cv2.drawContours(out_frame, [area_pts_right], -1, (255, 255, 255), -1)
        out_frame = cv2.bitwise_and(frame, out_frame)

        out_frame = frame[:, frame.shape[1] // 2:]

        cv2.imshow(name, out_frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            exit()

def capture_frame(queue1, queue2):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        queue1.put(frame.copy())
        queue2.put(frame.copy())
        time.sleep(0.01)  # Puedes ajustar el sleep si es necesario
    cap.release()
    queue1.put(None)
    queue2.put(None)

def process_frame(queue, process_name, function):
    while True:
        frame = queue.get()
        if frame is None:
            break
        function(process_name, frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    queue1 = Queue()
    queue2 = Queue()

    process1 = Process(target=process_frame, args=(queue1, "Entrada", in_function))
    process2 = Process(target=process_frame, args=(queue2, "Salida", out_function))
    capture_process = Process(target=capture_frame, args=(queue1, queue2))

    process1.start()
    process2.start()
    capture_process.start()

    process1.join()
    process2.join()
    capture_process.join()

    cv2.destroyAllWindows()