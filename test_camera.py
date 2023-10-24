"""
Main script for processing license plate detection and recognition with OAK-1 POE.
"""
import cv2
import sys
import depthai as dai
from sort.sort import *
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
from util import http_post, get_vehicles, read_license_plate, delete_files_in_directory, similarity_percentage
mot_tracker = Sort()


def main():
    """
    Main function of the script.
    """
    pipeline = dai.Pipeline()

    camRgb = pipeline.create(dai.node.ColorCamera)
    xoutVideo = pipeline.create(dai.node.XLinkOut)

    xoutVideo.setStreamName("video")

    camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(1920, 1080)
    camRgb.setFps(40)

    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)

    camRgb.video.link(xoutVideo.input)

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    last_checked_hour = None

    model_path = Path(__file__).parent / "model" / "yolov8n.pt"
    license_plate_path = Path(__file__).parent / "model" / "best.pt"

    nnPath = sys.argv[1] if len(sys.argv) > 1 else str(model_path)

    if not Path(nnPath).exists():
        raise FileNotFoundError(f'El modelo requerido no se encuentra en {nnPath}')

    if not license_plate_path.exists():
        raise FileNotFoundError(f'El modelo de placa de licencia no se encuentra en {license_plate_path}')

    coco_model = YOLO('model/yolov8n.pt')
    license_plate_model = YOLO('model/best.pt')

    vehicles = [2, 5, 6, 7]
    results = {}
    last_license_plate = None
    frame_nmr = 0

    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        while True:
            videoIn = video.get()

            frame = videoIn.getCvFrame()

            results[frame_nmr] = {}
            detections = coco_model(frame)[0]
            detections_ = []

            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, conf, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, conf, class_id])

            vehicles_ids = mot_tracker.update(np.array(detections_))
            width = frame.shape[1]
            mid_width = width // 2

            license_plates = license_plate_model(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                print(score)
                if score >= 0.7:
                    if x1 < mid_width:
                        direction = "entrada"
                    else:
                        direction = "salida"

                    xvehi1, yvehi1, xvehi2, yvehi2, vehi_ids = get_vehicles(license_plate, vehicles_ids)

                    vehicle_crop = frame[int(yvehi1):int(yvehi2), int(xvehi1):int(xvehi2), :]

                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                    license_plate_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_gray, 0, 255,
                                                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                    license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)

                    vehicle_img_name = f"vehicle_{current_time}.jpg"
                    cv2.imwrite(f"photos/vehicles/{vehicle_img_name}", vehicle_crop)

                    if license_plate_text is not None:
                        if last_license_plate is not None and license_plate_text is not None:
                            similarity = similarity_percentage(last_license_plate, license_plate_text)
                            if similarity > 70:
                                print("¡La patente actual es muy similar a la anterior! No se procesará.")
                                continue
                        results[frame_nmr][vehi_ids] = {'vehicle': {
                            'bbox': [xvehi1, yvehi1, xvehi2, yvehi2], },
                            'license_plate': {
                                'bbox': [x1, y1, x2, y2],
                                'text': license_plate_text,
                                'bbox_score': score,
                                'text_score': license_plate_score,
                                'direction': direction
                            }
                        }
                        print("License plate:", license_plate_text)
                        print("Detected with", "{:.2f}".format(license_plate_score * 100), "% confidence")
                        last_license_plate = license_plate_text

                        license_plate_img_name = f"license_plate_{license_plate_text}_{current_time}.jpg"
                        cv2.imwrite(f"photos/license_plate/{license_plate_img_name}", license_plate_crop)

                        http_post(license_plate_score, license_plate_img_name, vehicle_img_name,
                                  license_plate_text, direction)

            current_hour = datetime.now().hour
            current_minute = datetime.now().minute
            if current_hour == 12 and current_minute == 5 and current_hour != last_checked_hour:
                delete_files_in_directory("photos/license_plate")
                delete_files_in_directory("photos/vehicles")
                last_checked_hour = current_hour

            cv2.imshow("video", frame)
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == '__main__':
    main()
