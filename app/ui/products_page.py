"""
Products Page.
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
    QHeaderView,
)

from app.database.session import get_session
from app.services.product_service import ProductService
from app.ui.product_dialog import ProductDialog


class ProductsPage(QWidget):
    """Products Management Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = ProductService(self.session)

        self.build_ui()
        self.load_products()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        self.setWindowTitle("Products")

        layout = QVBoxLayout(self)

        title = QLabel("Products")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        layout.addWidget(title)

        # ---------------- Toolbar ----------------

        toolbar = QHBoxLayout()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(
            "Search by Name / SKU..."
        )
        self.search_edit.textChanged.connect(
            self.search_products
        )

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_product)
        self.delete_btn.clicked.connect(self.delete_product)
        self.refresh_btn.clicked.connect(
            self.load_products
        )

        toolbar.addWidget(self.search_edit)
        toolbar.addStretch()
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addWidget(self.refresh_btn)

        layout.addLayout(toolbar)

        # ---------------- Table ----------------

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "SKU",
                "Name",
                "Category",
                "Purchase",
                "Selling",
                "GST %",
                "Unit",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.doubleClicked.connect(
            self.edit_product
        )

        layout.addWidget(self.table)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)
            # --------------------------------------------------
    # Load Products
    # --------------------------------------------------

    def load_products(self):

        try:

            products = self.service.get_all()

            self.table.setRowCount(len(products))

            for row, product in enumerate(products):

                category = ""

                if getattr(product, "category", None):
                    category = product.category.name

                values = [
                    product.id,
                    product.sku,
                    product.name,
                    category,
                    f"{product.purchase_price:.2f}",
                    f"{product.selling_price:.2f}",
                    f"{product.gst_percent:.2f}",
                    product.unit,
                ]

                for col, value in enumerate(values):

                    item = QTableWidgetItem(str(value))

                    if col == 0:
                        item.setTextAlignment(Qt.AlignCenter)

                    self.table.setItem(row, col, item)

            self.status.setText(
                f"Total Products : {len(products)}"
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Products",
                str(exc),
            )

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search_products(self):

        keyword = (
            self.search_edit.text()
            .strip()
            .lower()
        )

        for row in range(self.table.rowCount()):

            visible = False

            for col in range(
                self.table.columnCount()
            ):

                item = self.table.item(row, col)

                if (
                    item
                    and keyword
                    in item.text().lower()
                ):
                    visible = True
                    break

            if keyword == "":
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(
                    row,
                    not visible,
                )

    # --------------------------------------------------
    # Selected Product
    # --------------------------------------------------

    def selected_product(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        product_id = int(
            self.table.item(row, 0).text()
        )

        return self.service.get(product_id)

    def selected_product_id(self):

        product = self.selected_product()

        if product is None:
            return None

        return product.id
        # --------------------------------------------------
    # Add Product
    # --------------------------------------------------

    def add_product(self):

        try:

            dialog = ProductDialog(parent=self)

            if dialog.exec():

                self.load_products()

                self.status.setText(
                    "Product added successfully."
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Add Product",
                str(exc),
            )

    # --------------------------------------------------
    # Edit Product
    # --------------------------------------------------

    def edit_product(self):

        product = self.selected_product()

        if product is None:

            QMessageBox.information(
                self,
                "Products",
                "Please select a product.",
            )

            return

        try:

            dialog = ProductDialog(
                product=product,
                parent=self,
            )

            if dialog.exec():

                self.load_products()

                self.status.setText(
                    "Product updated successfully."
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Edit Product",
                str(exc),
            )

    # --------------------------------------------------
    # Delete Product
    # --------------------------------------------------

    def delete_product(self):

        product = self.selected_product()

        if product is None:

            QMessageBox.information(
                self,
                "Products",
                "Please select a product.",
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Product",
            f"Delete '{product.name}' ?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete_product(product.id)

            self.load_products()

            self.status.setText(
                "Product deleted successfully."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Delete Product",
                str(exc),
            )