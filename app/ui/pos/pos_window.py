"""
POS Billing Window
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLineEdit,
    QLabel,
    QPushButton,
    QTableView,
    QFrame,
    QComboBox,
)

from app.ui.pos.pos_table_model import POSTableModel
from app.ui.pos.pos_controller import POSController
from app.ui.pos.loyalty_widget import LoyaltyWidget
from app.ui.pos.barcode_widget import BarcodeWidget
class POSWindow(QWidget):

    def __init__(self, session):

        super().__init__()

        self.session = session

        self.model = POSTableModel()

        self.controller = POSController(
            self,
            session,
        )

        self.build_ui()

        self.connect_signals()
    def create_header(self):

        layout = QHBoxLayout()

        self.bill_no = QLineEdit()

        self.customer = QComboBox()

        self.search = QLineEdit()

        self.barcode = BarcodeWidget()
        "Barcode / Product Name"
    )

    layout.addWidget(QLabel("Bill"))

    layout.addWidget(self.bill_no)

    layout.addWidget(QLabel("Customer"))

    layout.addWidget(self.customer)

    layout.addWidget(self.search)

    return layout

def create_table(self):

    self.table = QTableView()

    self.table.setModel(self.model)

    self.table.horizontalHeader().setStretchLastSection(True)

    return self.table

def create_right_panel(self):

    frame = QFrame()

    layout = QVBoxLayout(frame)

    self.loyalty = LoyaltyWidget()

    layout.addWidget(self.loyalty)

    layout.addStretch()

    return frame

def create_footer(self):

    layout = QHBoxLayout()

    self.btn_hold = QPushButton("Hold")

    self.btn_payment = QPushButton("Payment")

    self.btn_print = QPushButton("Print")

    self.btn_save = QPushButton("Save")

    layout.addWidget(self.btn_hold)

    layout.addWidget(self.btn_payment)

    layout.addWidget(self.btn_print)

    layout.addStretch()

    layout.addWidget(self.btn_save)

    return layout

def build_ui(self):

    root = QVBoxLayout(self)

    root.addLayout(self.create_header())

    splitter = QSplitter()

    splitter.addWidget(self.create_table())

    splitter.addWidget(self.create_right_panel())

    splitter.setStretchFactor(0,3)

    splitter.setStretchFactor(1,1)

    root.addWidget(splitter)

    root.addLayout(self.create_footer())

def connect_signals(self):

    self.barcode.barcodeScanned.connect(
        self.controller.scan_barcode
    )

    self.search.returnPressed.connect(

        self.controller.search_product

    )

    self.btn_payment.clicked.connect(

        self.controller.payment

    )

    self.btn_hold.clicked.connect(

        self.controller.hold_bill

    )

    self.btn_save.clicked.connect(

        self.controller.save_bill

    )    