@echo off
cd /d %~dp0
start http://localhost:8090
python app.py
pause
