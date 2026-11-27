@echo off
rem TMP Check - create (or reset) the operator account. Run once.
cd /d "%~dp0"
title TMP Check - operator account
python -m pip install -q -r requirements.txt
set /p OPNAME=Your name: 
set /p OPEMAIL=Operator email (not one already used in the portal): 
echo You will now be asked for a password (10+ characters). Nothing shows while you type.
python -m src.portal.devseed --org "TMP Check" --user "%OPNAME%" --email "%OPEMAIL%" --role admin
pause
