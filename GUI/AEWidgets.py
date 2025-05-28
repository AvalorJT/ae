from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import (
    QListWidget
)
class AEDraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True) # This enables the drag support for the list itself

    def startDrag(self, supportedActions: Qt.DropActions) -> None: # type: ignore
        # This method is automatically called by Qt when a drag gesture is detected.
        # 'supportedActions' typically comes from the QListWidget's default behavior,
        # but we customize what data is put into the QMimeData.

        item = self.currentItem() # Get the currently selected item
        if not item:
            return

        mime_data = QMimeData()
        # Set the text data for the drag operation. This is what the drop target will read.
        mime_data.setText(item.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        # Use Qt.CopyAction for dropping a new item, Qt.MoveAction if you want to remove from list
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)