@echo off
C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe src\resources.qrc -o src\resources_rc.py
call :iter
goto :eof

:iter
for %%f in (*.ui) do pyside-uic %%~dpnxf -o %%~dpf\ui_%%~nf.py
  for /D %%d in (*) do (
    cd %%d
    call :iter
    cd ..
  )
exit /b
