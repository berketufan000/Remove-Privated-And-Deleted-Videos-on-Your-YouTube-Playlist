@echo off
echo Starting the script...
pip install -r requirements.txt > NUL 2>&1
python script.py
echo Script finished.
pause