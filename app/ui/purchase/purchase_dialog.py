"""
Purchase Entry Dialog
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.ui.models.purchase_table_model import PurchaseTableModel
from app.ui.purchase.purchase_summary_widget import PurchaseSummaryWidget

class PurchaseDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Purchase Entry")

        self.resize(1400, 850)

        self.model = PurchaseTableModel()

        self.build_ui()

        self.connect_signals()
    def build_ui(self):

        root = QVBoxLayout(self)

        root.addWidget(self.create_header())

        root.addWidget(self.create_table(), 1)

        root.addWidget(self.create_footer())
def create_header(self):

    box = QGroupBox("Purchase Details")

    layout = QFormLayout(box)

    self.purchase_no = QLineEdit()
    self.invoice_no = QLineEdit()

    self.purchase_date = QDateEdit()

    self.purchase_date.setCalendarPopup(True)

    self.supplier = QComboBox()

    layout.addRow("Purchase No", self.purchase_no)
    layout.addRow("Invoice No", self.invoice_no)
    layout.addRow("Date", self.purchase_date)
    layout.addRow("Supplier", self.supplier)

    return box    
def create_table(self):

    self.table = QTableView()

    self.table.setModel(self.model)

    self.table.horizontalHeader().setStretchLastSection(True)

    self.table.setAlternatingRowColors(True)

    return self.table
def create_footer(self):

    widget = QWidget()

    layout = QHBoxLayout(widget)

    self.summary = PurchaseSummaryWidget()

    self.btn_add = QPushButton("Add Item")

    self.btn_remove = QPushButton("Remove Item")

    self.btn_save = QPushButton("Save")

    self.btn_print = QPushButton("Print")

    self.btn_close = QPushButton("Close")

    buttons = QVBoxLayout()

    buttons.addWidget(self.btn_add)

    buttons.addWidget(self.btn_remove)

    buttons.addStretch()

    buttons.addWidget(self.btn_save)

    buttons.addWidget(self.btn_print)

    buttons.addWidget(self.btn_close)

    layout.addWidget(self.summary)

    layout.addLayout(buttons)

    return widget
def connect_signals(self):

    self.btn_add.clicked.connect(

        self.model.add_item

    )

    self.btn_remove.clicked.connect(

        self.remove_current_row

    )

    self.btn_close.clicked.connect(

        self.close

    )
def remove_current_row(self):

    index = self.table.currentIndex()

    if not index.isValid():

        return

    self.model.remove_item(index.row())
    