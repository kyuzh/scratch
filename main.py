import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPathItem, \
    QGraphicsTextItem, QGraphicsItem, QMenu, QAction, QMainWindow, QWidget, QVBoxLayout, QFileDialog, \
    QGraphicsPolygonItem, QScrollArea

from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QPolygonF
import subprocess

class BlockItem(QGraphicsRectItem):
    def __init__(self, text, ordre, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, 100, 40)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptDrops(True)
        self.bloc_name = text
        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setDefaultTextColor(Qt.black)
        font = QFont("Arial", 10, QFont.Bold)
        self.text_item.setFont(font)
        self.text_item.setPos(5, 10)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            value.setX(round(value.x() / 20) * 20)
            value.setY(round(value.y() / 20) * 20)
        return super().itemChange(change, value)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()
        item = event.source()
        pos = self.scenePos()
        if isinstance(item, BlockItem) and item != self:
            line = ArrowItem(item, self)
            self.scene().addItem(line)

    def mouseDoubleClickEvent(self, event):
        print(self.bloc_name)
        file_path = "C:\\Users\\MAO\\Desktop\\test.txt"
        subprocess.Popen(['notepad.exe', file_path])

class ArrowItem(QGraphicsPathItem):
    def __init__(self, start_block, end_block):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPen(Qt.black)
        self.arrow_head = None
        self.start_block = start_block
        self.end_block = end_block

        self.update_position()

    def update_position(self):
        start_pos = self.start_block.scenePos() + QPointF(self.start_block.rect().width() / 2, self.start_block.rect().height())
        end_pos = self.end_block.scenePos() + QPointF(self.end_block.rect().width() / 2, 0)

        path = QPainterPath(start_pos)
        path.lineTo((start_pos + end_pos) / 2)  # Draw a line to the midpoint between start and end
        path.lineTo(end_pos)  # Draw a line to the end

        # Set the path for the arrow
        self.setPath(path)

        # Draw arrowhead at the end of the line
        arrow_size = 10
        angle = QLineF(start_pos, end_pos).angle()
        arrow_p1 = end_pos - QPointF(arrow_size * 0.6, 0)
        arrow_p2 = end_pos - QPointF(arrow_size * 0.6, arrow_size * 0.3)
        arrow_p3 = end_pos - QPointF(0, arrow_size * 0.3)

        arrow_polygon = QPolygonF([end_pos, arrow_p1, arrow_p2, arrow_p3])
        self.arrow_head = QGraphicsPolygonItem(arrow_polygon, self)
        self.arrow_head.setBrush(Qt.black)
        self.arrow_head.setFlag(QGraphicsItem.ItemIsSelectable)
        self.arrow_head.setZValue(1)


class ProgrammingView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.blocks = []

        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setSceneRect(0, 0, 2000, 2000)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.arrow_start_block = None
        self.temp_arrow = None

    def show_context_menu(self, pos):
        menu = QMenu(self)
        add_arrow_action = menu.addAction('Add Arrow')
        selected_action = menu.exec_(self.mapToGlobal(pos))

        if selected_action == add_arrow_action and self.arrow_start_block:
            self.temp_arrow = ArrowItem(self.arrow_start_block, self.arrow_start_block)  # Create a temporary arrow
            self.scene().addItem(self.temp_arrow)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if isinstance(item, BlockItem):
                self.arrow_start_block = item
                self.setCursor(Qt.CrossCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.temp_arrow:
            end_pos = self.mapToScene(event.pos())
            self.temp_arrow.update_position(self.arrow_start_block, end_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if isinstance(item, BlockItem) and item != self.arrow_start_block:
                if self.temp_arrow:
                    self.temp_arrow.end_block = item
                    self.temp_arrow.setFlag(QGraphicsItem.ItemIsSelectable)
                    self.temp_arrow.setZValue(0)
                    self.temp_arrow = None
            else:
                self.scene().removeItem(self.temp_arrow)
            self.arrow_start_block = None
            self.unsetCursor()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, BlockItem):
            if self.arrow_start_block is None:
                self.arrow_start_block = item
                self.setCursor(Qt.CrossCursor)
            else:
                end_block = item
                arrow_item = ArrowItem(self.arrow_start_block, end_block)
                self.scene().addItem(arrow_item)
                self.arrow_start_block = None
                self.unsetCursor()

class ScratchLikeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Scratch-Like')
        self.setGeometry(100, 100, 2000, 2000)

        container = QWidget(self)
        layout = QVBoxLayout(container)

        # Créez une zone de défilement (scroll area)
        scroll_area = QScrollArea(self)
        self.programming_view = ProgrammingView(self)

        # Ajoutez la vue de la scène à la zone de défilement
        scroll_area.setWidget(self.programming_view)
        layout.addWidget(scroll_area)

        block1 = BlockItem('Move Forward',1)
        block1.setPos(100, 100)
        self.programming_view.scene().addItem(block1)

        block2 = BlockItem('Turn Right',2)
        block2.setPos(100, 200)
        self.programming_view.scene().addItem(block2)

        block3 = BlockItem('start',3)
        block3.setPos(100, 50)
        self.programming_view.scene().addItem(block3)

        layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_all_blocks(self):
        for block in self.blocks:
            block.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScratchLikeApp()
    window.show()
    sys.exit(app.exec_())
