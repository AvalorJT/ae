import os, json
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QToolBar,
    QLabel,
    QComboBox, # NEW: Import QComboBox
    QSizePolicy, # NEW: For toolbar spacing
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QKeySequence 
from GUI.Viewports.OutputViewport import OutputViewport

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Automation Engine")
        self.setGeometry(100, 100, 800, 600)

        self.config_data = {}

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Top Menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")
        self.setMenuBar(menu_bar)

 # --- Toolbar - MODIFIED ORDER ---
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar) # Add the toolbar to the QMainWindow early

        # Load configuration data first, as comboboxes depend on it
        self._load_config()

        # 1. API ComboBox
        toolbar.addWidget(QLabel("  API: "))
        self.api_combobox = QComboBox(self)
        self.api_combobox.setFixedWidth(150)
        self.api_combobox.currentIndexChanged.connect(self._update_environment_combobox)
        toolbar.addWidget(self.api_combobox)

        # 2. Environment ComboBox
        toolbar.addWidget(QLabel("  Env: "))
        self.env_combobox = QComboBox(self)
        self.env_combobox.setFixedWidth(100)
        self.env_combobox.currentIndexChanged.connect(self._update_tenant_combobox)
        toolbar.addWidget(self.env_combobox)

        # 3. Tenant ComboBox
        toolbar.addWidget(QLabel("  Tenant: "))
        self.tenant_combobox = QComboBox(self)
        self.tenant_combobox.setFixedWidth(150)
        toolbar.addWidget(self.tenant_combobox)

        # Initial population of comboboxes after they are created and connected
        self._populate_api_combobox() # This will trigger subsequent updates

        # 4. Visual Separator
        toolbar.addWidget(self._create_toolbar_separator()) # <--- REPLACED addSeparator() with this call

        # 5. Play Button
        play_action = QAction(QIcon.fromTheme("media-playback-start"), "Play", self)
        toolbar.addAction(play_action)


        # Add a stretch to push toolbar items to the left (if you want them left-aligned with free space to the right)
        # If you want it to push the play button to the far right, put it before the play button.
        # If you want it to push everything to the left, keep it here.
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        # --- END Toolbar Modifications ---

        # Main Content Area (Node Library + Blueprint Viewport)
        main_content_layout = QHBoxLayout()

        # API Call List (QListWidget, no drag)
        self.api_list = QListWidget()
        self.api_list.addItem("Get User Data")
        self.api_list.addItem("Process User Data")
        self.api_list.addItem("Log Activity")
        self.api_list.setFixedWidth(200)
        # Note: We'll add selection signal for ActionViewport later
        main_content_layout.addWidget(self.api_list)
        
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

        close_action = QAction("Close Application", self) # Give it a descriptive name
        
        # 2. Set the shortcut to the Escape key
        # Qt.Key.Key_Escape is the enum for the Escape key
        # QKeySequence wraps it for shortcut assignment
        close_action.setShortcut(QKeySequence(Qt.Key.Key_Escape))
        
        # 3. Connect the action's 'triggered' signal to the QMainWindow's 'close' slot
        # The 'close' slot will gracefully close the window (and thus the application).
        close_action.triggered.connect(self.close)
        
        # 4. Add the action to the main window. This registers the shortcut.
        self.addAction(close_action)
        

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'config.json')
        try:
            with open(config_path, 'r') as f:
                self.config_data = json.load(f)
            print("Config loaded successfully!")
        except FileNotFoundError:
            print(f"Error: config.json not found at {config_path}")
            self.config_data = {}
        except json.JSONDecodeError:
            print(f"Error: config.json has invalid JSON format at {config_path}")
            self.config_data = {}

    def _create_toolbar_separator(self):
        separator = QWidget(self)
        separator.setFixedWidth(7) # Let's keep your 3px width
        # Match toolbar height dynamically or use a fixed reasonable value
        # Access self.toolbar after it's been added
        # If toolbar is already fully initialized and has a height
        separator.setFixedHeight(13)

        # Style the separator: a dark gray background with a subtle border
        # --- ADDED MARGIN TO THE SEPARATOR ITSELF ---
        separator.setStyleSheet("background-color: #555; border: 2px solid #444; margin-left: 7px;") # 10px margin on the left
        # --- END ADDED MARGIN ---
        return separator
    
    def _populate_api_combobox(self):
        self.api_combobox.blockSignals(True)
        self.api_combobox.clear()
        apis: dict = self.config_data.get("apis", {})
        if apis:
            self.api_combobox.addItems(sorted(apis.keys()))
        self.api_combobox.blockSignals(False)
        self._update_environment_combobox()  # Trigger update for environment combobox

    def _update_environment_combobox(self):
        selected_api = self.api_combobox.currentText()
        self.env_combobox.blockSignals(True)
        self.env_combobox.clear()
        if selected_api and "apis" in self.config_data and selected_api in self.config_data["apis"]:
            api_details = self.config_data["apis"][selected_api]
            if "environments" in api_details:
                environments = sorted(api_details["environments"].keys())
                self.env_combobox.addItems(environments)
        self.env_combobox.blockSignals(False)
        self._update_tenant_combobox() # Trigger update for tenant

    def _update_tenant_combobox(self):
        selected_api = self.api_combobox.currentText()
        selected_env = self.env_combobox.currentText()
        self.tenant_combobox.blockSignals(True)
        self.tenant_combobox.clear()

        # --- FIX: Access tenants through "apis:", "environments", and "tenants" keys ---
        if selected_api and selected_env and \
           "apis" in self.config_data and \
           selected_api in self.config_data["apis"] and \
           "environments" in self.config_data["apis"][selected_api]: # Check that 'environments' key exists

            environments_data = self.config_data["apis"][selected_api]["environments"]
            if selected_env in environments_data: # <--- CRITICAL NEW CHECK: Does the selected_env actually exist?
                env_details:dict = environments_data[selected_env]
                if env_details and "tenants" in env_details:
                    tenants_data = env_details.get("tenants", {})
                    tenants = sorted(tenants_data.keys())
                    self.tenant_combobox.addItems(tenants)
        self.tenant_combobox.blockSignals(False)


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