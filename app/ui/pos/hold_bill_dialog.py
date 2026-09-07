"""
Hold Bill Dialog
Commercial POS Version
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)


class HoldBillDialog(QDialog):

    billSelected = Signal(int)

    def __init__(self, controller, parent=None):

        super().__init__(parent)

        self.controller = controller

        self.bills = []

        self.setWindowTitle("Held Bills")

        self.resize(1000, 600)

        self.build_ui()

        self.connect_signals()

        self.load_bills()

    # -------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        top = QHBoxLayout()

        top.addWidget(QLabel("Search"))

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Bill No / Customer / Mobile"
        )

        top.addWidget(self.search)

        root.addLayout(top)

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([

            "Bill No",

            "Customer",

            "Items",

            "Amount",

            "Time",

            "Cashier",

            "Status",

        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        root.addWidget(self.table)

        buttons = QHBoxLayout()

        self.btn_resume = QPushButton("Resume Bill")

        self.btn_delete = QPushButton("Delete")

        self.btn_close = QPushButton("Close")

        buttons.addStretch()

        buttons.addWidget(self.btn_resume)

        buttons.addWidget(self.btn_delete)

        buttons.addWidget(self.btn_close)

        root.addLayout(buttons)

    # -------------------------------------------------

    def connect_signals(self):

        self.search.textChanged.connect(

            self.filter_bills

        )

        self.btn_resume.clicked.connect(

            self.resume_bill

        )

        self.btn_delete.clicked.connect(

            self.delete_bill

        )

        self.btn_close.clicked.connect(

            self.reject

        )

        self.table.doubleClicked.connect(

            self.resume_bill

        )

    # -------------------------------------------------

    def load_bills(self):

        self.bills = self.controller.sale_service.get_hold_bills()

        self.populate(self.bills)

    # -------------------------------------------------

    def populate(self, bills):

        self.table.setRowCount(len(bills))

        for row, bill in enumerate(bills):

            self.table.setItem(
                row, 0,
                QTableWidgetItem(bill.bill_no)
            )

            self.table.setItem(
                row, 1,
                QTableWidgetItem(bill.customer_name)
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(str(bill.item_count))
            )

            self.table.setItem(
                row, 3,
                QTableWidgetItem(
                    f"{bill.grand_total:.2f}"
                )
            )

            self.table.setItem(
                row, 4,
                QTableWidgetItem(
                    bill.bill_time.strftime("%H:%M")
                )
            )

            self.table.setItem(
                row, 5,
                QTableWidgetItem(
                    bill.cashier_name
                )
            )

            self.table.setItem(
                row, 6,
                QTableWidgetItem(
                    bill.status
                )
            )

    # -------------------------------------------------

    def filter_bills(self):

        text = self.search.text().lower()

        if not text:

            self.populate(self.bills)

            return

        result = []

        for bill in self.bills:

            if (

                text in bill.bill_no.lower()

                or text in bill.customer_name.lower()

                or text in bill.customer_mobile.lower()

            ):

                result.append(bill)

        self.populate(result)

    # -------------------------------------------------

    def current_bill(self):

        row = self.table.currentRow()

        if row < 0:

            return None

        bill_no = self.table.item(row,0).text()

        return self.controller.sale_service.get_hold_bill(
            bill_no
        )

    # -------------------------------------------------

    def resume_bill(self):

        bill = self.current_bill()

        if bill is None:

            return

        self.billSelected.emit(bill.id)

        self.accept()

    # -------------------------------------------------

    def delete_bill(self):

        bill = self.current_bill()

        if bill is None:

            return

        reply = QMessageBox.question(

            self,

            "Delete",

            f"Delete Hold Bill {bill.bill_no} ?"

        )

        if reply != QMessageBox.Yes:

            return

        self.controller.sale_service.delete_hold_bill(

            bill.id

        )

        self.load_bills()