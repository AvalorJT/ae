from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QBrush, QColor, QPen, QFont, QFontMetrics
from PySide6.QtCore import Qt, QRectF, QPointF

class ApiCallNode(QGraphicsItem):
    def __init__(self, name="API Call", parent=None):
        super().__init__(parent)
        self.name = name
        self.width = 100
        self.height = 50
        self.title_bar_height = 20
        self.port_radius = 5
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height,
        )

    def paint(self, painter, option, widget):
        # Node body
        body_rect = QRectF(
            -self.width / 2,
            -self.height / 2 + self.title_bar_height,
            self.width,
            self.height - self.title_bar_height,
        )
        body_brush = QBrush(QColor(220, 220, 220))
        body_pen = QPen(QColor(100, 100, 100))
        painter.fillRect(body_rect, body_brush)
        painter.drawRect(body_rect)

        # Title bar
        title_rect = QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.title_bar_height,
        )
        title_brush = QBrush(QColor(150, 150, 150))
        title_pen = QPen(QColor(80, 80, 80))
        painter.fillRect(title_rect, title_brush)
        painter.drawRect(title_rect)

        # Node name text
        font = QFont("Arial", 10)
        painter.setFont(font)
        text_rect = title_rect.adjusted(5, 2, -5, -2)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)

        # Input port (left)
        input_port_pos = QPointF(-self.width / 2 - self.port_radius, 0)
        painter.setBrush(QBrush(QColor(100, 150, 255)))
        painter.setPen(QPen(QColor(50, 100, 200)))
        painter.drawEllipse(input_port_pos, self.port_radius, self.port_radius)

        # Output port (right)
        output_port_pos = QPointF(self.width / 2 + self.port_radius, 0)
        painter.setBrush(QBrush(QColor(255, 150, 100)))
        painter.setPen(QPen(QColor(200, 100, 50)))
        painter.drawEllipse(output_port_pos, self.port_radius, self.port_radius)