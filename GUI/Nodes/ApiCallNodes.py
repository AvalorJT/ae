from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QBrush, QColor, QPen, QFont, QFontMetrics, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF

class ApiCallNode(QGraphicsItem):
    def __init__(self, name="API Call", parent=None):
        super().__init__(parent)
        self.name = name
        self.port_radius = 5
        self.horizontal_padding = 20 # Padding around text
        self.vertical_padding = 10  # Padding around text
        self.title_bar_height = 20

        # Calculate initial size based on text  
        font = QFont("Arial", 10)
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(self.name)
        text_height = metrics.height()

        self.width = max(100, text_width + self.horizontal_padding * 2) # Min width of 100
        self.height = text_height + self.title_bar_height + self.vertical_padding * 2 # Min height based on text

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges) # Often useful, but boundingRect fix is more direct
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache) # Could help performance, but might hide issues if boundingRect is wrong

    def boundingRect(self):
        # The bounding rectangle must fully encompass all drawn elements, including ports
        # and a small buffer for anti-aliasing.
        # A port (circle) centered at X +/- radius extends 'radius' further in that direction.
        # Its center is at (width/2 + port_radius) from node center.
        # Its outermost edge is (width/2 + port_radius) + port_radius = width/2 + 2*port_radius.
        antialiasing_buffer = 4 # A small buffer for anti-aliasing artifacts

        # Calculate max horizontal extent from node's center (0,0) to rightmost point of right port
        max_x_extent = self.width / 2 + (2 * self.port_radius) + antialiasing_buffer
        # Max vertical extent from node's center (0,0) to topmost/bottommost point of node/ports
        # Assuming ports are vertically centered relative to node's center (Y=0)
        # The node body itself extends self.height/2 vertically from its own center.
        # The ports are centered at Y=0, so their vertical extent is port_radius.
        max_y_extent = self.height / 2 + self.port_radius + antialiasing_buffer

        return QRectF(
            -max_x_extent,
            -max_y_extent,
            2 * max_x_extent, # Total width of bounding box
            2 * max_y_extent, # Total height of bounding box
        )


    def paint(self, painter, option, widget):
        # Set antialiasing for smoother drawing
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Node body
        body_rect = QRectF(
            -self.width / 2,
            -self.height / 2 + self.title_bar_height,
            self.width,
            self.height - self.title_bar_height,
        )
        body_brush = QBrush(QColor(220, 220, 220))
        body_pen = QPen(QColor(100, 100, 100))
        painter.setBrush(body_brush)
        painter.setPen(body_pen)
        painter.drawRect(self.boundingRect())

        # Title bar
        title_rect = QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.title_bar_height,
        )
        title_brush = QBrush(QColor(150, 150, 150))
        title_pen = QPen(QColor(80, 80, 80))
        painter.setBrush(title_brush)
        painter.setPen(title_pen)
        painter.drawRect(title_rect)

        # Node name text
        font = QFont("Arial", 10)
        painter.setFont(font)
        # Calculate text position within the title bar
        # Adjust text_rect to be within the title_rect
        text_rect = title_rect.adjusted(self.horizontal_padding, 0, -self.horizontal_padding, 0)
        # Center the text vertically within the title bar
        text_rect.moveCenter(title_rect.center())
        painter.setPen(QColor(0, 0, 0)) # Set text color to black for contrast
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, self.name)

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