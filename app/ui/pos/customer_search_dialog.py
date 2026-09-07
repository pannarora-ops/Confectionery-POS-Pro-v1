"""
Customer Search Dialog
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
    QTableWidget,
    QTableWidgetItem,
    QLabel,
)


class CustomerSearchDialog(QDialog):

    customerSelected = Signal(object)

    def __init__(self, controller, parent=None):

        super().__init__(parent)

        self.controller = controller

        self.customers = []

        self.setWindowTitle("Customer Search")

        self.resize(850, 550)

        self.build_ui()

        self.connect_signals()

        self.load_customers()

    # -------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        search_layout = QHBoxLayout()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search Name / Mobile / Customer Code"
        )

        self.btn_new = QPushButton("New Customer")

        search_layout.addWidget(QLabel("Search"))

        search_layout.addWidget(self.search)

        search_layout.addWidget(self.btn_new)

        root.addLayout(search_layout)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([

            "Code",

            "Customer",

            "Mobile",

            "Points",

            "Credit",

            "Level",

        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        root.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.btn_select = QPushButton("Select")

        self.btn_cancel = QPushButton("Cancel")

        button_layout.addStretch()

        button_layout.addWidget(self.btn_select)

        button_layout.addWidget(self.btn_cancel)

        root.addLayout(button_layout)

    # -------------------------------------------------

    def connect_signals(self):

        self.search.textChanged.connect(
            self.filter_customers
        )

        self.table.doubleClicked.connect(
            self.select_customer
        )

        self.btn_select.clicked.connect(
            self.select_customer
        )

        self.btn_cancel.clicked.connect(
            self.reject
        )

    # -------------------------------------------------

    def load_customers(self):

        self.customers = self.controller.customer_service.get_all()

        self.populate_table(self.customers)

    # -------------------------------------------------

    def populate_table(self, customers):

        self.table.setRowCount(len(customers))

        for row, customer in enumerate(customers):

            self.table.setItem(
                row, 0,
                QTableWidgetItem(customer.customer_code)
            )

            self.table.setItem(
                row, 1,
                QTableWidgetItem(customer.name)
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(customer.mobile)
            )

            self.table.setItem(
                row, 3,
                QTableWidgetItem(str(customer.loyalty_points))
            )

            self.table.setItem(
                row, 4,
                QTableWidgetItem(f"{customer.credit_balance:.2f}")
            )

            self.table.setItem(
                row, 5,
                QTableWidgetItem(customer.membership_level)
            )

    # -------------------------------------------------

    def filter_customers(self):

        text = self.search.text().lower()

        if not text:

            self.populate_table(self.customers)

            return

        filtered = []

        for customer in self.customers:

            if (

                text in customer.name.lower()

                or text in customer.mobile.lower()

                or text in customer.customer_code.lower()

            ):

                filtered.append(customer)

        self.populate_table(filtered)

    # -------------------------------------------------

    def select_customer(self):

        row = self.table.currentRow()

        if row < 0:

            return

        code = self.table.item(row, 0).text()

        customer = self.controller.customer_service.get_by_code(code)

        self.customerSelected.emit(customer)

        self.accept()