from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QToolBar,
    QLabel
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from GUI.Viewports.BlueprintViewport import BlueprintViewport
from GUI.Viewports.OutputViewport import OutputViewport

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Automation Engine")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Top Menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")
        self.setMenuBar(menu_bar)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        play_action = QAction(QIcon.fromTheme("media-playback-start"), "Play", self)
        stop_action = QAction(QIcon.fromTheme("media-playback-stop"), "Stop", self)
        toolbar.addAction(play_action)
        toolbar.addAction(stop_action)
        self.addToolBar(toolbar)

        # Main Content Area (Node Library + Blueprint Viewport)
        main_content_layout = QHBoxLayout()

        # API Call Library
        self.api_library = QListWidget()
        self.api_library.addItem("Get User Data")
        self.api_library.addItem("Process User Data")
        self.api_library.addItem("Log Activity")
        main_content_layout.addWidget(self.api_library)

        
        # Action Viewport (Placeholder for now)
        # This will later be replaced by your custom ActionViewport widget
        self.action_viewport_placeholder = QLabel("Action Viewport: Detailed API Call Configuration")
        self.action_viewport_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_content_layout.addWidget(self.action_viewport_placeholder, 1) # Stretch factor to take up space

        main_layout.addLayout(main_content_layout, 1) # Stretch factor for the main content area



        # Output View
        self.output_viewport = OutputViewport()
        self.output_viewport.command_entered.connect(self.handle_shell_command)
        main_layout.addWidget(self.output_viewport,0)

        self.setCentralWidget(central_widget)
        
    def handle_shell_command(self, command):
        # This is where you'll process commands from the shell
        if command.lower() == "help":
            self.output_viewport.append_output("Available commands: help, clear, echo <text>")
        elif command.lower() == "clear":
            self.output_viewport.output_display.clear()
        elif command.lower().startswith("echo "):
            self.output_viewport.append_output(command[5:])
        else:
            self.output_viewport.append_output(f"Unknown command: {command}")