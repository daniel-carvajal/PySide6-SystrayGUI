# Remove existing build artifacts (delete any files or directories that were created the last time the build script was run)
rm -r build dist
rm app.spec
rm resources.py

# Convert the resources.qrc file into a Python module named resources.py using pyside6-rcc tool.
pyside6-rcc resources.qrc -o resources.py