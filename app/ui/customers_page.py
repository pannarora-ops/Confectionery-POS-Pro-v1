"""
Customers Page.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)

from app.database.session import get_session
from app.services.customer_service import CustomerService
from app.ui.customer_dialog import CustomerDialog


class CustomersPage(QWidget):
    """Customers Management Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = CustomerService(self.session)

        self.build_ui()
        self.load_customers()

    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Customers")
        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        layout.addWidget(title)

        # ---------------------------------------
        # Toolbar
        # ---------------------------------------

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search customer..."
        )
        self.search.textChanged.connect(
            self.search_customers
        )

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(
            self.add_customer
        )

        edit_btn.clicked.connect(
            self.edit_customer
        )

        delete_btn.clicked.connect(
            self.delete_customer
        )

        refresh_btn.clicked.connect(
            self.load_customers
        )

        toolbar.addWidget(self.search)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # ---------------------------------------
        # Table
        # ---------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Phone",
                "Email",
                "GST",
                "Address",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        self.table.doubleClicked.connect(
            self.edit_customer
        )

        layout.addWidget(self.table)

        self.status = QLabel()

        layout.addWidget(self.status)

    # --------------------------------------------------

    def load_customers(self):

        customers = self.service.get_all()

        self.table.setRowCount(
            len(customers)
        )

        for row, customer in enumerate(customers):

            values = [
                customer.id,
                customer.name,
                customer.phone or "",
                customer.email or "",
                getattr(
                    customer,
                    "gst_number",
                    "",
                ),
                customer.address or "",
            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                if col == 0:
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                self.table.setItem(
                    row,
                    col,
                    item,
                )

        self.status.setText(
            f"Total Customers : {len(customers)}"
        )

    # --------------------------------------------------

    def search_customers(self):

        text = (
            self.search.text()
            .lower()
            .strip()
        )

        for row in range(
            self.table.rowCount()
        ):

            visible = False

            for col in range(
                self.table.columnCount()
            ):

                item = self.table.item(
                    row,
                    col,
                )

                if (
                    item
                    and text
                    in item.text().lower()
                ):
                    visible = True
                    break

            self.table.setRowHidden(
                row,
                False if text == "" else not visible,
            )

    # --------------------------------------------------

    def selected_customer_id(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return int(
            self.table.item(
                row,
                0,
            ).text()
        )

    # --------------------------------------------------

    def add_customer(self):

        dialog = CustomerDialog(
            parent=self
        )

        if dialog.exec():
            self.load_customers()

    # --------------------------------------------------

    def edit_customer(self):

        customer_id = self.selected_customer_id()

        if customer_id is None:

            QMessageBox.warning(
                self,
                "Customers",
                "Select a customer.",
            )

            return

        customer = self.service.get(
            customer_id
        )

        if customer is None:

            QMessageBox.warning(
                self,
                "Customers",
                "Customer not found.",
            )

            return

        dialog = CustomerDialog(
            customer=customer,
            parent=self,
        )

        if dialog.exec():

            self.load_customers()

    # --------------------------------------------------

    def delete_customer(self):

        customer_id = self.selected_customer_id()

        if customer_id is None:

            QMessageBox.warning(
                self,
                "Customers",
                "Select a customer.",
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Customer",
            "Delete selected customer?",
            QMessageBox.Yes |
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete(
                customer_id
            )

            self.session.commit()

            self.load_customers()

        except Exception as exc:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )