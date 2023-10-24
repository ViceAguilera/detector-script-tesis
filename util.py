"""
Module containing utility functions.
"""
import json
import base64
import shutil
import easyocr
import requests
from sort.sort import *
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
        if text.isalnum() and score >= 0.5 and not text.isalpha():
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


def delete_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename == ".gitkeep":
            continue

        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Error al eliminar {file_path}. Razón: {e}')


def similarity_percentage(str1, str2):
    str1_set = set(str1)
    str2_set = set(str2)

    common_chars = str1_set.intersection(str2_set)
    total_chars = str1_set.union(str2_set)

    return (len(common_chars) / len(total_chars)) * 100
