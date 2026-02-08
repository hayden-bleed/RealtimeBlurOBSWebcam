@echo off
cd /d %~dp0
call .venv\Scripts\activate
python blur_virtual_cam.py
pause