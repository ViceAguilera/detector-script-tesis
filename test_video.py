"""
Main script for processing license plate detection and recognition with video.
"""
import cv2
import json
import base64
import easyocr
import requests
from sort.sort import *
from ultralytics import YOLO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
mot_tracker = Sort()
reader = easyocr.Reader(['en'], gpu=False)


def http_post(score, license_img_name, vehicle_img_name, text, direction):
    """
    Send a POST request to the API.

    Args:
        score (float): Confidence score of the license plate text.
        license_img_name (str): Name of the license plate image file.
        vehicle_img_name (str): Name of the vehicle image file.
        text (str): License plate text.
        direction (str): Direction of the vehicle.

    Returns:
        None
    """
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    url = f"http://{host}:{port}/api/registers"
    vehicle_image_encoded = encode_image_to_base64("photos/vehicles/" + vehicle_img_name)
    license_plate_image_encoded = encode_image_to_base64("photos/license_plate/" + license_img_name)

    data = {
        "licensePlate": text,
        "predictionAccuracy": score,
        "type": direction,
        "vehicleImage": vehicle_image_encoded,
        "licensePlateImage": license_plate_image_encoded
    }

    print(data)

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json_data, headers=headers, timeout=10)

        if response.status_code == 200:
            print("The request was sent successfully.")
        else:
            print(response.status_code)
            print("An error occurred while sending the request.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP POST request: {e}")


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
    for vehicle in vehicles_ids:
        xvehi1, yvehi1, xvehi2, yvehi2, vehi_id = vehicle
        if x1 >= xvehi1 and x2 <= xvehi2 and y1 >= yvehi1 and y2 <= yvehi2:
            return vehicle
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
        if text.isalnum() and score >= 0.6 and not text.isalpha():
            return text, score

    return None, None


def encode_image_to_base64(image_path):
    """
    Encode image to base64.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    print(encoded_string)
    return encoded_string


def main():
    """
    Main function of the script.
    """
    cap = cv2.VideoCapture("test.mp4")
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    coco_model = YOLO('model/yolov8n.pt')
    license_plate_model = YOLO('model/best.pt')

    vehicles = [2, 5, 6, 7]
    results = {}
    last_license_plate = None
    frame_nmr = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

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
                    if last_license_plate is not None and license_plate_text == last_license_plate:
                        print("¡Same license plate as before detected!")
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

        cv2.imshow("video", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
