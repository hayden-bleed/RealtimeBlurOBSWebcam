import cv2
import numpy as np
import pyvirtualcam

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---- SETTINGS YOU CAN TUNE ----
CAM_INDEX = 0              # 0 is usually default webcam
MIN_CONFIDENCE = 0.6       # face detection confidence
BLUR_STRENGTH = 45         # must be odd number: 25/35/45/55 etc.
PADDING = 0.25             # expand the face box a bit (0.15–0.35 good)
TARGET_FPS = 30            # virtual cam FPS
VIRTUAL_CAM_NAME = None    # set to "OBS Virtual Camera" if needed
# --------------------------------

def odd(n: int) -> int:
    return n if n % 2 == 1 else n + 1

BLUR_STRENGTH = odd(BLUR_STRENGTH)

MODEL_PATH = "blaze_face_short_range.tflite"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceDetectorOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    min_detection_confidence=MIN_CONFIDENCE,
)
detector = vision.FaceDetector.create_from_options(options)


cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)  # CAP_DSHOW helps on Windows
if not cap.isOpened():
    raise RuntimeError("Could not open webcam. Try changing CAM_INDEX.")

# Read one frame to get size
ok, frame = cap.read()
if not ok:
    raise RuntimeError("Could not read from webcam.")
h, w = frame.shape[:2]

# Create virtual camera
cam_kwargs = {}
if VIRTUAL_CAM_NAME:
    cam_kwargs["device"] = VIRTUAL_CAM_NAME

with pyvirtualcam.Camera(width=w, height=h, fps=TARGET_FPS, fmt=pyvirtualcam.PixelFormat.BGR, **cam_kwargs) as vcam:
    print(f"Virtual cam started: {vcam.device} ({w}x{h} @ {TARGET_FPS}fps)")
    print("Press CTRL+C in this window to stop.")

    timestamp_ms = 0 

    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        # Convert to RGB for MediaPipe Tasks
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Wrap frame for MediaPipe Tasks
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # MediaPipe VIDEO mode requires a monotonic timestamp in ms
        timestamp_ms += int(1000 / TARGET_FPS)
        
        result = detector.detect_for_video(mp_image, timestamp_ms)

        if result.detections:
            for det in result.detections:
                bbox = det.bounding_box

                x1, y1 = bbox.origin_x, bbox.origin_y
                bw, bh = bbox.width, bbox.height
                x2, y2 = x1 + bw, y1 + bh

                # Add padding
                pad_x = int(bw * PADDING)
                pad_y = int(bh * PADDING)

                x1p = max(0, x1 - pad_x)
                y1p = max(0, y1 - pad_y)
                x2p = min(w, x2 + pad_x)
                y2p = min(h, y2 + pad_y)

                roi = frame[y1p:y2p, x1p:x2p]
                if roi.size > 0:
                    blurred = cv2.GaussianBlur(roi, (BLUR_STRENGTH, BLUR_STRENGTH), 0)
                    frame[y1p:y2p, x1p:x2p] = blurred

        vcam.send(frame)
        vcam.sleep_until_next_frame()