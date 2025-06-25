cd /d "%~dp0"
@rem Place this batch file in the same folder as download.py.

python -m pip install requests 
python -m pip install pyinstaller
if not exist dist python -m PyInstaller -F download.py

@echo off
set integration-key=<integration key here>
@echo on

@rem Set current-date to be the current date
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set current-date=%%c-%%a-%%b)

dist\download.exe "%integration-key%" "2024-01-01" "%current-date%" "output" --audit_report
pause