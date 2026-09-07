"""
Suppliers Page.
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
from app.services.supplier_service import SupplierService
from app.ui.supplier_dialog import SupplierDialog


class SuppliersPage(QWidget):
    """Suppliers Management Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = SupplierService(self.session)

        self.build_ui()
        self.load_suppliers()

    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Suppliers")
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search supplier..."
        )
        self.search.textChanged.connect(
            self.search_suppliers
        )

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(self.add_supplier)
        edit_btn.clicked.connect(self.edit_supplier)
        delete_btn.clicked.connect(self.delete_supplier)
        refresh_btn.clicked.connect(self.load_suppliers)

        toolbar.addWidget(self.search)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

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
            self.edit_supplier
        )

        layout.addWidget(self.table)

        self.status = QLabel()
        layout.addWidget(self.status)

    # --------------------------------------------------

    def load_suppliers(self):

        suppliers = self.service.get_all()

        self.table.setRowCount(len(suppliers))

        for row, supplier in enumerate(suppliers):

            values = [
                supplier.id,
                supplier.name,
                supplier.phone or "",
                supplier.email or "",
                getattr(
                    supplier,
                    "gst_number",
                    "",
                ),
                supplier.address or "",
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
            f"Total Suppliers : {len(suppliers)}"
        )

    # --------------------------------------------------

    def search_suppliers(self):

        text = self.search.text().lower().strip()

        for row in range(self.table.rowCount()):

            visible = False

            for col in range(self.table.columnCount()):

                item = self.table.item(row, col)

                if item and text in item.text().lower():
                    visible = True
                    break

            self.table.setRowHidden(
                row,
                False if text == "" else not visible,
            )

    # --------------------------------------------------

    def selected_supplier_id(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return int(
            self.table.item(row, 0).text()
        )

    # --------------------------------------------------

    def add_supplier(self):

        dialog = SupplierDialog(parent=self)

        if dialog.exec():
            self.load_suppliers()

    # --------------------------------------------------

    def edit_supplier(self):

        supplier_id = self.selected_supplier_id()

        if supplier_id is None:

            QMessageBox.warning(
                self,
                "Suppliers",
                "Select a supplier.",
            )

            return

        supplier = self.service.get(
            supplier_id
        )

        if supplier is None:

            QMessageBox.warning(
                self,
                "Suppliers",
                "Supplier not found.",
            )

            return

        dialog = SupplierDialog(
            supplier=supplier,
            parent=self,
        )

        if dialog.exec():
            self.load_suppliers()

    # --------------------------------------------------

    def delete_supplier(self):

        supplier_id = self.selected_supplier_id()

        if supplier_id is None:

            QMessageBox.warning(
                self,
                "Suppliers",
                "Select a supplier.",
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Supplier",
            "Delete selected supplier?",
            QMessageBox.Yes |
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete(
                supplier_id
            )

            self.session.commit()

            self.load_suppliers()

        except Exception as exc:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )