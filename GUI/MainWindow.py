import os, json, inspect, importlib
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
        self.config_data = {}
        self.synced_api_name = None # To track the name of the currently synced API
        self.current_api_instance = None
        self._load_config()

        self.setWindowTitle("Automation Engine")
        self.setGeometry(100, 100, 800, 600)

        # Load configuration data first, as comboboxes depend on it

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Top Menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")
        self.setMenuBar(menu_bar)

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar) # Add the toolbar to the QMainWindow early


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

        self.sync_action = QAction(QIcon.fromTheme("view-refresh"), "Sync API", self)
        self.sync_action.setEnabled(False) # Disabled by default
        self.sync_action.triggered.connect(self._sync_api)
        toolbar.addAction(self.sync_action)
        # 5. Play Button
        play_action = QAction(QIcon.fromTheme("media-playback-start"), "Play", self)
        toolbar.addAction(play_action)


        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        # -- Main Content Area (Node Library + Blueprint Viewport) --
        main_content_layout = QHBoxLayout()

        # API Call List (QListWidget, no drag)
        self.api_list = QListWidget()
        self.api_list.setFixedWidth(200)
        #self._update_api_actions_list()
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
        close_action.setShortcut(QKeySequence(Qt.Key.Key_Escape))
        close_action.triggered.connect(self.close)
        
        # Main Window Actions
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

        # Style the separator: a dark gray background with a subtle border and margin
        separator.setStyleSheet("background-color: #555; border: 2px solid #444; margin-left: 7px;") # 10px margin on the left
        return separator
    
    def _populate_api_combobox(self):
        self.api_combobox.blockSignals(True)
        self.api_combobox.clear()
        apis: dict = self.config_data.get("apis", {})
        if apis:
            self.api_combobox.addItems(sorted(apis.keys()))
        if self.api_combobox.count() > 0:
            self.api_combobox.setCurrentIndex(-1) # Default to no selection
        else:
            # If no APIs, ensure dependent UI is also cleared/disabled
            self._update_environment_combobox() # This will cascade to clear others
        self.api_combobox.blockSignals(False)

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
        # Enable/disable sync button based on API selection
        if hasattr(self, 'sync_action'):
            can_sync = bool(selected_api) and (selected_api != self.synced_api_name)
            self.sync_action.setEnabled(can_sync)

        self._update_tenant_combobox() # Trigger update for tenant
        # self._update_api_actions_list() # Moved to be called by _update_tenant_combobox

    def _update_tenant_combobox(self):
        selected_api = self.api_combobox.currentText()
        selected_env = self.env_combobox.currentText()
        self.tenant_combobox.blockSignals(True)
        self.tenant_combobox.clear()

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
        self._update_api_actions_list() #

    def _update_api_actions_list(self):
        """
        Populates the api_list QListWidget with methods from the selected API
        that are marked with the _is_api_call attribute.
        """
        self.api_list.clear()
        selected_api_name = self.api_combobox.currentText()

        if not selected_api_name:
            return

        api_config = self.config_data.get("apis", {}).get(selected_api_name)
        if not api_config or "module" not in api_config or "class" not in api_config:
            # self.output_viewport.append_output(f"Config for API '{selected_api_name}' missing module/class.")
            print(f"Config for API '{selected_api_name}' missing module/class.")
            return

        module_name = api_config["module"]
        class_name = api_config["class"]

        try:
            module = importlib.import_module(module_name)
            api_class = getattr(module, class_name)

            for member_name, member_obj in inspect.getmembers(api_class):
                if inspect.isfunction(member_obj) and hasattr(member_obj, '_is_api_call') and member_obj._is_api_call: # type: ignore[attr-defined]
                    friendly_name = member_name.replace('_', ' ').title()
                    self.api_list.addItem(friendly_name)
        except ImportError:
            self.output_viewport.append_output(f"Error: Could not import API module {module_name}")
            print(f"Error: Could not import module {module_name}")
        except AttributeError:
            self.output_viewport.append_output(f"Error: Could not find API class {class_name} in {module_name}")
            print(f"Error: Could not find class {class_name} in module {module_name}")
        except Exception as e:
            self.output_viewport.append_output(f"Error loading actions for {selected_api_name}: {e}")


    def _sync_api(self):
        selected_api_name = self.api_combobox.currentText()
        if not selected_api_name:
            self.output_viewport.append_output("No API selected to sync.")
            return

        api_config = self.config_data.get("apis", {}).get(selected_api_name)
        if not api_config or "module" not in api_config or "class" not in api_config:
            self.output_viewport.append_output(f"Configuration for API '{selected_api_name}' is missing module/class details.")
            self.current_api_instance = None
            return

        # Assume failure for synced_api_name until successful instantiation
        original_synced_name = self.synced_api_name # Store in case we need to revert or for logic
        self.synced_api_name = None # Tentatively clear, will be set on success
        module_name = api_config["module"]
        class_name = api_config["class"]

        try:
            self.output_viewport.append_output(f"Syncing API: {selected_api_name}...")
            module = importlib.import_module(module_name)
            api_class = getattr(module, class_name)
            self.current_api_instance = api_class() # Instantiate the API
            self.synced_api_name = selected_api_name # Mark this API as successfully synced
            self.output_viewport.append_output(f"Successfully synced and instantiated API: {selected_api_name} ({class_name})")
            # You might want to do more here, like passing environment-specific config to the API instance
            # For example: self.current_api_instance.configure(self.env_combobox.currentText(), self.tenant_combobox.currentText())
        except ImportError:
            self.output_viewport.append_output(f"Error: Could not import API module '{module_name}'.")
            self.current_api_instance = None
            # self.synced_api_name remains None (or what it was cleared to)
        except AttributeError:
            self.output_viewport.append_output(f"Error: Could not find API class '{class_name}' in module '{module_name}'.")
            self.current_api_instance = None
            # self.synced_api_name remains None
        except Exception as e:
            self.output_viewport.append_output(f"Error instantiating API '{selected_api_name}': {e}")
            self.current_api_instance = None
            # self.synced_api_name remains None
        finally:
            # Refresh button states, especially the sync button, based on the outcome
            self._update_environment_combobox()

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