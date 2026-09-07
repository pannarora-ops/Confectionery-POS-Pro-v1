from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProductsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Products Page")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
