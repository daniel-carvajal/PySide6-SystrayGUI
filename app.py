from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QColorDialog, QSystemTrayIcon, QMenu, QFileDialog

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("animal-dog.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Function to open file dialog


def open_file_dialog():
    file_name, _ = QFileDialog.getOpenFileName()
    if file_name:
        print("Selected file:", file_name)
        # Handle the file as needed


# Create the menu
menu = QMenu()

# Replace the color format actions with a file dialog action
file_action = QAction("Open File")
file_action.triggered.connect(open_file_dialog)
menu.addAction(file_action)

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()
