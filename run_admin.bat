@echo off
cd /d "%~dp0"
powershell -Command "Start-Process cmd -ArgumentList '/k python gui.py' -Verb RunAs"