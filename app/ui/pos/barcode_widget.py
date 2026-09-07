"""
Barcode Widget
Commercial POS Version
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class BarcodeWidget(QWidget):
    """
    Barcode Search Widget
    """

    barcodeScanned = Signal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()

        self.connect_signals()

    # -------------------------------------------------

    def build_ui(self):

        layout = QHBoxLayout(self)

        self.txtBarcode = QLineEdit()

        self.txtBarcode.setPlaceholderText(
            "Scan Barcode / Enter Product Code"
        )

        self.btnScan = QPushButton("📷 Camera")

        self.btnClear = QPushButton("✖")

        layout.addWidget(self.txtBarcode)

        layout.addWidget(self.btnScan)

        layout.addWidget(self.btnClear)

    # -------------------------------------------------

    def connect_signals(self):

        self.txtBarcode.returnPressed.connect(
            self.emit_barcode
        )

        self.btnClear.clicked.connect(
            self.clear
        )

        self.btnScan.clicked.connect(
            self.open_camera
        )

    # -------------------------------------------------

    def emit_barcode(self):

        barcode = self.txtBarcode.text().strip()

        if barcode:

            self.barcodeScanned.emit(barcode)

            self.txtBarcode.clear()

    # -------------------------------------------------

    def clear(self):

        self.txtBarcode.clear()

        self.txtBarcode.setFocus()

    # -------------------------------------------------

    def open_camera(self):

        """
        Camera scanner integration.

        Future implementation:
        - OpenCV
        - pyzbar
        - ZXing
        - Android Camera
        """

        print("Camera Scanner Coming Soon")

    # -------------------------------------------------

    def set_focus(self):

        self.txtBarcode.setFocus()