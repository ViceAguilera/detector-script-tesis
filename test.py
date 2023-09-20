import cv2
from ultralytics import YOLO
from sort.sort import *
import easyocr
import depthai as dai

mot_tracker = Sort()
reader = easyocr.Reader(['en'] , gpu=False)

def get_vehicles(license_plate, vehicles_ids):
    """
    Get the vehicles bounding boxes that are close to the license plate.

    Args:
        license_plate (list): List containing the license plate bounding box coordinates.
        vehicles_ids (list): List containing the vehicles bounding box coordinates.

    Returns:
        tuple: Tuple containing the vehicles bounding box coordinates that are close to the license plate.
    """

    x1, y1, x2, y2, score, class_id = license_plate

    for i in range(len(vehicles_ids)):
        xvehi1, yvehi1, xvehi2, yvehi2, vehi_id = vehicles_ids[i]
        if x1 > xvehi1 and x2 < xvehi2 and y1 > yvehi1 and y2 < yvehi2:
            car_index = i
            found = True
            break
    if found:
        return vehicles_ids[car_index]
    return -1, -1, -1, -1, -1

def read_license_plate(license_plate_crop_thresh):
    """
       Read the license plate text from the given cropped image.

       Args:
           license_plate_crop_thresh (numpy.ndarray): Cropped image containing the license plate.

       Returns:
           tuple: Tuple containing the formatted license plate text and its confidence score.
       """

    detections = reader.readtext(license_plate_crop_thresh)

    for detection in detections:
        _, text, score = detection

        text = text.upper().replace(' ', '')
        if len(text) >= 6 and len(text) <= 9 and text.isalnum() and score >= 0.7 and not text.isalpha():
            return text, score

    return None, None

def main():
    """
    Main function of the script.
    """

    #Create pipeline
    pipeline = dai.Pipeline()

    camRgb = pipeline.create(dai.node.ColorCamera)
    xoutVideo = pipeline.create(dai.node.XLinkOut)

    xoutVideo.setStreamName("video")

    camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)  # Set resolution
    camRgb.setVideoSize(1920, 1080)
    camRgb.setFps(40)

    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)

    camRgb.video.link(xoutVideo.input)  # Link video

    coco_model = YOLO('model/yolov8n.pt')
    license_plate_model = YOLO('model/licence_plate.pt')

    vehicles = [2, 5, 6, 7]
    results = {}
    last_license_plate = None
    frame_nmr = 0
    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)  # Get video output queue
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

            license_plates = license_plate_model(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                xvehi1, yvehi1, xvehi2, yvehi2, vehi_ids = get_vehicles(license_plate, vehicles_ids)

                license_plate_crop = frame[int():int(y2), int(x1):int(x2), :]
                license_plate_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                license_plate_text, license_plate_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    if last_license_plate is not None and license_plate_text == last_license_plate:
                        print("¡Same license plate as before detected!")
                        continue
                    results[frame_nmr][vehi_ids] = {'vehicle': {
                                                        'bbox': [xvehi1, yvehi1, xvehi2, yvehi2],},
                                                    'license_plate': {
                                                        'bbox': [x1, y1, x2, y2],
                                                        'text': license_plate_text,
                                                        'bbox_score': score,
                                                        'text_score': license_plate_score}
                    }
                    print("License plate:", license_plate_text)
                    print("Detected with", "{:.2f}".format(license_plate_score * 100), "% confidence")
            cv2.imshow("video", frame)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == '__main__':
    main()
