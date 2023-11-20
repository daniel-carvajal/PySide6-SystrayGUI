rm -r build dist
rm app.spec
rm resources.py
pyside6-rcc resources.qrc -o resources.py
# pyinstaller --windowed app.py