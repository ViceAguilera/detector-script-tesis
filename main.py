#!/usr/bin/env python3
import cv2
import depthai as dai
from ultralytics import YOLO

pipeline = dai.Pipeline() # Create pipeline

camRgb = pipeline.create(dai.node.ColorCamera) # Create Color Camera
xoutVideo = pipeline.create(dai.node.XLinkOut) # Create XLinkOut node

xoutVideo.setStreamName("video") # Set stream name

camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A) # Set camera socket
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P) # Set resolution
camRgb.setVideoSize(1920, 1080) # Set video size
camRgb.setFps(40) # Set fps

xoutVideo.input.setBlocking(False) # Set blocking
xoutVideo.input.setQueueSize(1) # Set queue size

camRgb.video.link(xoutVideo.input) # Link video

model = YOLO('model/licence_plate.pt')
results = {}
last_license_plate = None
frame_nmr = 0

with dai.Device(pipeline) as device:
    video = device.getOutputQueue(name="video", maxSize=1, blocking=False) # Get video output queue
    while True:
        videoIn = video.get()

        frame = videoIn.getCvFrame()

        results = model.track(frame, persist=True)

        frame_ = results[0].plot()

        cv2.imshow("video", frame_)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
