py -3.5 C:\Python35\Scripts\cxfreeze ark-eiui.py -OO --compress --target-dir=../ark-eiui-amd64 --icon=../arky/ark.ico --base-name=Win32GUI
C:\Users\Bruno\upx.exe --best ..\ark-eiui-amd64\python*.dll
C:\Users\Bruno\upx.exe --best ..\ark-eiui-amd64\*.pyd
py -3.5-32 C:\Python35\Scripts\cxfreeze ark-eiui.py -OO --compress --target-dir=../ark-eiui-win32 --icon=../arky/ark.ico --base-name=Win32GUI
C:\Users\Bruno\upx.exe --best ..\ark-eiui-win32\python*.dll
C:\Users\Bruno\upx.exe --best ..\ark-eiui-win32\*.pyd
