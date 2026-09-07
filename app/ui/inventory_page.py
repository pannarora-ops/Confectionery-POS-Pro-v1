from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class InventoryPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Inventory Page")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
