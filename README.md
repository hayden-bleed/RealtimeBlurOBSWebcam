# FaceblurCam

Real-time face-tracking blur for OBS using MediaPipe and a virtual webcam.

This project creates a virtual camera that blurs your face dynamically while streaming.
Designed to be simple to run for non-technical users.

## Features
- Real-time face detection
- Smooth face blur that follows movement
- Works with OBS via virtual camera
- One-click install and run (Windows)

## Requirements
- Windows
- Python 3.14+
- OBS Studio
- A webcam

## Download Options

### Download ZIP (Recommended for most users)
- Go to the **Releases** page
- Download the latest `.zip`
- Extract it
- Double-click `install.bat`, then `run.bat`
This options is best if you just want to use the tool.

## Setup (First Time Only)
1. Download or clone this repository
2. Double-click `install.bat`
3. Wait for dependencies to install

## Running
1. Plug in your webcam
2. Double-click `run.bat`
3. Open OBS
4. Add a **Video Capture Device**
5. Select **OBS Virtual Camera**

## Notes
- The virtual environment (`.venv`) is created locally and not included in the repo
- If the camera fails to open, make sure no other app is using it

## Credits
Built using OpenCV, MediaPipe Tasks, and pyvirtualcam.

