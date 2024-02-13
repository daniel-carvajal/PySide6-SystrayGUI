To build the application, follow these steps:

1. This shell script removes existing build artifacts (deletes any files or directories that were created the last time the build script was run) and then converts resources.qrc into a Python module using pyside6-rcc. 
```shell
- sudo ./build.sh
```
2. Run the following command to create a windowed executable using PyInstaller:
```shell
- pyinstaller --windowed app.py
```