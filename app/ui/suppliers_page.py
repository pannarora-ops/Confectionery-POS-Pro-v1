from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SuppliersPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Suppliers Page")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
