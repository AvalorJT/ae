from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit
)

class OutputViewport(QWidget): 
    command_entered = Signal(str) # Custom signal to emit when a command is entered
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Remove margins for a cleaner look

        # Output Display Area
        self.output_display = QTextEdit() # Use QTextEdit or QPlainTextEdit
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Output will appear here...")
        main_layout.addWidget(self.output_display)

        # Input Line
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.returnPressed.connect(self._on_return_pressed) # Connect Enter key press
        main_layout.addWidget(self.input_line)

        # Initial message
        self.append_output("Welcome to the Automation Engine Shell!")
        self.append_output("Type a command and press Enter.")

    def _on_return_pressed(self):
        command = self.input_line.text()
        if command:
            self.append_output(f"> {command}") # Echo the command
            self.command_entered.emit(command) # Emit the command for processing
            self.input_line.clear() # Clear the input line

    def append_output(self, text):
        self.output_display.append(text)
        self.output_display.verticalScrollBar().setValue(self.output_display.verticalScrollBar().maximum())
