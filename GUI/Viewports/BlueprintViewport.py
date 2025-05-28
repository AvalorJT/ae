from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from GUI.Nodes.ApiCallNodes import ApiCallNode
from PySide6.QtCore import Qt, QPointF

class BlueprintViewport(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.setAcceptDrops(True) # Enable drag and drop
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setSceneRect(-200, -200, 400, 400) # Define a larger scene area
        self.scale_factor = 1.0

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            print(f"Drag Enter Event: Accepted. Data: {event.mimeData().text()}")
        else:
            event.ignore()
            print(f"Drag Enter Event: Ignored. No text data.")

    # --- CRITICAL: Ensure this method is present and accepts the action ---
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("Drop event triggered (BlueprintViewport)") # This should now print!
        if event.mimeData().hasText():
            text = event.mimeData().text()
            node = ApiCallNode(name=text)
            scene_pos = self.mapToScene(event.position().toPoint())
            node.setPos(scene_pos)
            self.scene().addItem(node)
            event.acceptProposedAction()
            print(f"Node '{text}' added at {scene_pos}")
        else:
            event.ignore()
            print("Drop event: Ignored. No text data.")

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor
            if event.angleDelta().y() > 0:
                self.scale(zoom_in_factor, zoom_in_factor)
                self.scale_factor *= zoom_in_factor
            else:
                self.scale(zoom_out_factor, zoom_out_factor)
                self.scale_factor *= zoom_out_factor
            event.accept()
        else:
            super().wheelEvent(event)