import os
import sys
from pathlib import Path
import configparser

import resources  # Import the compiled resource file.
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QFileDialog, QLineEdit, QMessageBox



class MainWindow(QtWidgets.QMainWindow):
    def get_settings_dir(self):
        home_dir = Path.home()
        settings_dir = home_dir / '.pyside6_starter'
        settings_dir.mkdir(exist_ok=True) # Creates a directory if it doesn't already exist.
        filename = 'settings.ini'
        return settings_dir / filename
    
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()  # Load settings first
        self.config = {
            "app_name": "PySide6-SytrayGUI",
            "config_path": self.get_settings_dir(),
            "api_key": "API_KEY",
            "close_message": "Goodbye :)",
            "debug_mode": False,
            "interval": self.settings.get('interval', 1500) # Use settings value or default
        }

    def show_popup_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        # Use the resource
        icon_path = ":/icons/application_icon.png"
        msg_box.setIconPixmap(QIcon(icon_path).pixmap(64, 64))
        msg_box.exec()

    def show_settings_window(self):
        self.setWindowTitle("Settings")

        self.button = QtWidgets.QPushButton("Save")
        self.button.clicked.connect(self.on_button_clicked)

        # Create QLineEdit
        self.lineedit = QLineEdit()
        self.lineedit.setMaxLength(10)
        self.lineedit.setPlaceholderText("API Key")
        # emitted when the user hits the Enter or Return key while editing the line edit.
        self.lineedit.returnPressed.connect(self.return_pressed)
        # emitted whenever the selection of text within the line edit changes
        self.lineedit.selectionChanged.connect(self.selection_changed)
        # emitted whenever the text in the line edit changes. This can be due to user input or programmatic changes
        self.lineedit.textChanged.connect(self.text_changed)
        # emitted when the text is changed due to user input (not programmatic changes)
        self.lineedit.textEdited.connect(self.text_edited)

        h_layout = QtWidgets.QHBoxLayout()
        # Add line edit to the horizontal layout
        h_layout.addWidget(self.lineedit)
        h_layout.addWidget(self.button)  # Add button to the horizontal layout

        # [3. Create and set up QVBoxLayout]
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(l)  # Add the label to the vertical layout
        # Add the horizontal layout (line edit and button) to the vertical layout
        layout.addLayout(h_layout)

        # Create widgets for the new row
        new_label = QtWidgets.QLabel("Location of User Library")
        new_line_edit = QtWidgets.QLineEdit()
        new_line_edit.setReadOnly(True)
        # Replace with the actual default text
        new_line_edit.setText("/Users/.../Desktop/User Library")
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.open_file_dialog)

        # Create a QHBoxLayout for the label and browse button
        label_browse_layout = QtWidgets.QHBoxLayout()
        label_browse_layout.addWidget(new_label)
        label_browse_layout.addWidget(browse_button)

        # Create a QVBoxLayout for the new row
        v_layout_new_row = QtWidgets.QVBoxLayout()
        # Add the QHBoxLayout with label and button
        v_layout_new_row.addLayout(label_browse_layout)
        # Then the line edit underneath
        v_layout_new_row.addWidget(new_line_edit)

        # Adjust spacing and margins as needed
        # Decrease the spacing if needed, the default is usually around 6-9 depending on the platform
        v_layout_new_row.setSpacing(8)
        # v_layout_new_row.setContentsMargins(0, 0, 0, 0)  # Set to zero or a small number for tighter packing

        # Add the new QVBoxLayout to the existing QVBoxLayout
        layout.addLayout(v_layout_new_row)

        # Create a central widget and set the layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()
        self.raise_()
        self.activateWindow()

    # emitted when the user hits the Enter or Return key while editing the line edit.
    def return_pressed(self):
        print("Return pressed!")
        # self.lineedit.setText("BOOM!")

    # emitted whenever the selection of text within the line edit changes
    def selection_changed(self):
        print("Selection changed")
        print(self.lineedit.selectedText())

    # method that gets called in response to the textChanged signal. It's used to respond to any change in the text of the line edit.
    def text_changed(self, text):
        print("Text changed...")
        print(text)

    # method that handles the textEdited signal. It's specifically for responding to changes made by the user, excluding changes made programmatically
    def text_edited(self, text): 
        print("Text edited...")
        print(text)

    def get_data_path(self, filename):
        home_dir = Path.home()
        settings_dir = home_dir / '.pyside6_starter'
        settings_dir.mkdir(exist_ok=True)
        return settings_dir / filename

    def load_settings(self):
        settings_path = self.get_data_path('settings.ini')
        print(f"Looking for settings.ini at: {settings_path}")  # Debug print

        if not settings_path.exists():
            print("Settings file not found, creating from default settings.")
            local_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            default_settings_path = local_dir / 'default_settings.ini'
            # Debug print
            print(
                f"Looking for default_settings.ini at: {default_settings_path}")

            # Make sure the default settings file exists
            if not default_settings_path.exists():
                print("Default settings file not found.")
                return {}
            with open(default_settings_path, 'r') as default_settings, open(settings_path, 'w') as settings:
                settings.write(default_settings.read())
                # Debug print
                print(
                    f"Created settings.ini from default_settings.ini at: {settings_path}")

        config = configparser.ConfigParser()
        config.read(settings_path)

        # Here you can define the expected settings and their types
        settings_to_validate = {
            'General': {
                'interval': int,  # Add 'interval' to the 'General' section
            },
        }

        # Initialize an empty dictionary to hold settings
        validated_settings = {}

        # Validate and assign settings
        for section, settings in settings_to_validate.items():
            for setting, value_type in settings.items():
                if value_type == int:
                    validated_settings[setting] = config.getint(
                        section, setting, fallback=0)
                elif value_type == float:
                    validated_settings[setting] = config.getfloat(
                        section, setting, fallback=0.0)
                # Add more types if needed

        return validated_settings

    def update_settings(self, new_settings):
        settings_path = self.get_data_path('settings.ini')

        # Load the current settings
        config = configparser.ConfigParser()
        config.read(settings_path)

        # Update settings
        for section, settings in new_settings.items():
            if not config.has_section(section):
                config.add_section(section)
            for setting, value in settings.items():
                config.set(section, setting, str(value))

        # Write updated settings back to the file
        with open(settings_path, 'w') as configfile:
            config.write(configfile)
        print("Settings updated and saved to:", settings_path)

    def update_and_reload_settings(self, new_settings):
        self.update_settings(new_settings)
        self.settings = self.load_settings()

        # Dynamically update self.config based on the new settings
        for section, settings in new_settings.items():
            for setting, value in settings.items():
                if setting in self.config:
                    self.config[setting] = self.settings.get(
                        setting, self.config[setting])
        print("Settings updated, saved, and reloaded.")
        print(self.config)

    def on_button_clicked(self):
        print("Button clicked! API key updated")  # Replace with the action you want to perform
        self.show_popup_message("Success", "Your operation was successful!")
        # self.open_file_dialog()

    # Function to open file dialog
    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            print("Selected file:", file_name)
            # Handle the file as needed
            self.update_and_reload_settings({'General': {'interval': 1000}})

def start():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

    # icon = QIcon("animal-dog.png")
    icon = QIcon(':/icons/application_icon.png')

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    def open_settings_window():
        w.show_settings_window()

    # The menu bar items list (Enable, Settings, Quit) is not considered a window. 
    # It's a context menu associated with the system tray icon. When you click the 
    # system tray icon, this context menu is displayed.
    
    menu = QMenu()

    mic_action = QAction("Enable")
    menu.addAction(mic_action)

    settings_action = QAction("Settings")
    settings_action.triggered.connect(open_settings_window)
    menu.addAction(settings_action)

    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec()

if __name__ == '__main__':
    start();