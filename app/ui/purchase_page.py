"""
Purchase Page.
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
from app.services.report_service import ReportService
from app.ui.purchase_dialog import PurchaseDialog


class PurchasePage(QWidget):
    """Purchase Management Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.report = ReportService(self.session)

        self.build_ui()
        self.load_purchases()

    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Purchases")
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search Invoice..."
        )
        self.search.textChanged.connect(
            self.search_purchase
        )

        add_btn = QPushButton("New Purchase")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(
            self.add_purchase
        )

        refresh_btn.clicked.connect(
            self.load_purchases
        )

        toolbar.addWidget(self.search)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Invoice",
                "Supplier",
                "Date",
                "Items",
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

        layout.addWidget(self.table)

        self.status = QLabel()

        layout.addWidget(self.status)

    # -------------------------------------------------

    def load_purchases(self):

        purchases = self.report.purchases()

        self.table.setRowCount(
            len(purchases)
        )

        for row, purchase in enumerate(purchases):

            values = [
                purchase.id,
                purchase.invoice_number,
                purchase.supplier.name
                if purchase.supplier
                else "",
                purchase.purchase_date.strftime(
                    "%d-%m-%Y"
                ),
                len(purchase.items),
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
            f"Total Purchases : {len(purchases)}"
        )

    # -------------------------------------------------

    def search_purchase(self):

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

    # -------------------------------------------------

    def add_purchase(self):

        dialog = PurchaseDialog(self)

        if dialog.exec():

            self.load_purchases()

    # -------------------------------------------------

    def selected_purchase(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return int(
            self.table.item(
                row,
                0,
            ).text()
        )