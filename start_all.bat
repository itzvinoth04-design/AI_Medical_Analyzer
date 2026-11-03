@echo off
echo ================================================================
echo  Launching MediGuide AI Platform (Backend + Frontend)
echo ================================================================
start "MediGuide AI - Backend Server" cmd /k "cd /d %~dp0backend && python run.py"
timeout /t 3 /nobreak >nul
start "MediGuide AI - Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"
echo Both servers launched! Open http://localhost:5173 in your browser.
pause
