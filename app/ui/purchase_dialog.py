"""
Purchase Dialog.
"""

from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from app.database.session import get_session
from app.services.product_service import ProductService
from app.services.purchase_service import PurchaseService
from app.services.supplier_service import SupplierService


class PurchaseDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.session = get_session()

        self.purchase_service = PurchaseService(self.session)
        self.product_service = ProductService(self.session)
        self.supplier_service = SupplierService(self.session)

        self.items = []

        self.setWindowTitle("New Purchase")
        self.resize(900, 650)

        self.build_ui()

    # -----------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.invoice = QLineEdit()

        self.supplier = QComboBox()

        for supplier in self.supplier_service.get_all():
            self.supplier.addItem(
                supplier.name,
                supplier.id,
            )

        self.remarks = QTextEdit()

        form.addRow(
            "Invoice",
            self.invoice,
        )

        form.addRow(
            "Supplier",
            self.supplier,
        )

        form.addRow(
            "Remarks",
            self.remarks,
        )

        layout.addLayout(form)

        # ---------------------------

        grid = QGridLayout()

        self.product = QComboBox()

        for product in self.product_service.get_all():

            self.product.addItem(
                product.name,
                product.id,
            )

        self.qty = QSpinBox()
        self.qty.setMaximum(100000)

        self.rate = QDoubleSpinBox()
        self.rate.setMaximum(9999999)
        self.rate.setDecimals(2)

        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(
            self.add_item
        )

        grid.addWidget(
            QLabel("Product"),
            0,
            0,
        )

        grid.addWidget(
            self.product,
            0,
            1,
        )

        grid.addWidget(
            QLabel("Qty"),
            0,
            2,
        )

        grid.addWidget(
            self.qty,
            0,
            3,
        )

        grid.addWidget(
            QLabel("Rate"),
            0,
            4,
        )

        grid.addWidget(
            self.rate,
            0,
            5,
        )

        grid.addWidget(
            add_btn,
            0,
            6,
        )

        layout.addLayout(grid)

        # ---------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Product",
                "Qty",
                "Rate",
                "Amount",
            ]
        )

        layout.addWidget(self.table)

        # ---------------------------

        self.total = QLabel("Total : ₹ 0.00")

        layout.addWidget(self.total)

        # ---------------------------

        buttons = QHBoxLayout()

        save = QPushButton("Save Purchase")
        cancel = QPushButton("Cancel")

        save.clicked.connect(
            self.save_purchase
        )

        cancel.clicked.connect(
            self.reject
        )

        buttons.addStretch()

        buttons.addWidget(save)
        buttons.addWidget(cancel)

        layout.addLayout(buttons)

    # -----------------------------------------------------

    def add_item(self):

        product_name = self.product.currentText()
        product_id = self.product.currentData()

        qty = Decimal(str(self.qty.value()))
        rate = Decimal(str(self.rate.value()))

        if qty <= 0:
            return

        self.items.append(
            {
                "product_id": product_id,
                "name": product_name,
                "quantity": qty,
                "rate": rate,
            }
        )

        self.refresh_table()

    # -----------------------------------------------------

    def refresh_table(self):

        self.table.setRowCount(
            len(self.items)
        )

        total = Decimal("0")

        for row, item in enumerate(self.items):

            amount = (
                item["quantity"]
                * item["rate"]
            )

            total += amount

            values = [
                item["name"],
                item["quantity"],
                item["rate"],
                amount,
            ]

            for col, value in enumerate(values):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    ),
                )

        self.total.setText(
            f"Total : ₹ {total:.2f}"
        )

    # -----------------------------------------------------

    def save_purchase(self):

        if not self.invoice.text():

            QMessageBox.warning(
                self,
                "Purchase",
                "Invoice number required.",
            )

            return

        if not self.items:

            QMessageBox.warning(
                self,
                "Purchase",
                "Add at least one item.",
            )

            return

        try:

            self.purchase_service.create_purchase(
                invoice_number=self.invoice.text(),
                supplier_id=self.supplier.currentData(),
                items=self.items,
                remarks=self.remarks.toPlainText(),
            )

            QMessageBox.information(
                self,
                "Success",
                "Purchase Saved.",
            )

            self.accept()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )