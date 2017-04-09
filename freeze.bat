py -3.5 C:\Python35\Scripts\cxfreeze ark-eiui.py -OO --compress --target-dir=../app/ark-eiui-amd64 --icon=ark.ico --base-name=Win32GUI
C:\Users\Bruno\upx.exe --best ..\app\ark-eiui-amd64\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\ark-eiui-amd64\*.pyd
py -3.5-32 C:\Python35\Scripts\cxfreeze ark-eiui.py -OO --compress --target-dir=../app/ark-eiui-win32 --icon=ark.ico --base-name=Win32GUI
C:\Users\Bruno\upx.exe --best ..\app\ark-eiui-win32\python*.dll
C:\Users\Bruno\upx.exe --best ..\app\ark-eiui-win32\*.pyd
