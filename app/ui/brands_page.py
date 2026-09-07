"""
Brands Page.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database.session import get_session
from app.services.brand_service import BrandService
from app.ui.brand_dialog import BrandDialog


class BrandsPage(QWidget):
    """Brand Master."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = BrandService(self.session)

        self.build_ui()
        self.load_brands()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Brand Master")

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        # ---------------------------------------

        toolbar = QHBoxLayout()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search Brand..."
        )

        self.search.textChanged.connect(
            self.search_brand
        )

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(self.add_brand)
        edit_btn.clicked.connect(self.edit_brand)
        delete_btn.clicked.connect(self.delete_brand)
        refresh_btn.clicked.connect(self.load_brands)

        toolbar.addWidget(self.search)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # ---------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Brand",
            "Description",
            "Products",
            "Status",
        ])

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
            self.edit_brand
        )

        layout.addWidget(self.table)

        self.status = QLabel()

        layout.addWidget(self.status)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load_brands(self):

        brands = self.service.get_all()

        self.table.setRowCount(len(brands))

        for row, brand in enumerate(brands):

            values = [

                brand.id,

                brand.name,

                brand.description or "",

                len(brand.products),

                "Active" if brand.active else "Inactive",

            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(str(value))

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
            f"Total Brands : {len(brands)}"
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search_brand(self):

        text = self.search.text().lower()

        for row in range(self.table.rowCount()):

            visible = False

            for col in range(
                self.table.columnCount()
            ):

                item = self.table.item(row, col)

                if (
                    item
                    and text in item.text().lower()
                ):
                    visible = True
                    break

            self.table.setRowHidden(
                row,
                False if text == "" else not visible,
            )

    # -------------------------------------------------
    # Selected
    # -------------------------------------------------

    def selected_brand_id(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return int(
            self.table.item(row, 0).text()
        )

    # -------------------------------------------------
    # Add
    # -------------------------------------------------

    def add_brand(self):

        dialog = BrandDialog(parent=self)

        if dialog.exec():

            self.load_brands()

    # -------------------------------------------------
    # Edit
    # -------------------------------------------------

    def edit_brand(self):

        brand_id = self.selected_brand_id()

        if brand_id is None:

            QMessageBox.warning(
                self,
                "Brand",
                "Select a brand.",
            )

            return

        brand = self.service.get(
            brand_id
        )

        if brand is None:

            QMessageBox.warning(
                self,
                "Brand",
                "Brand not found.",
            )

            return

        dialog = BrandDialog(
            brand,
            self,
        )

        if dialog.exec():

            self.load_brands()

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_brand(self):

        brand_id = self.selected_brand_id()

        if brand_id is None:

            QMessageBox.warning(
                self,
                "Brand",
                "Select a brand.",
            )

            return

        reply = QMessageBox.question(

            self,

            "Delete Brand",

            "Delete selected brand?",

            QMessageBox.Yes |
            QMessageBox.No,

        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete(
                brand_id
            )

            self.session.commit()

            self.load_brands()

        except Exception as exc:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )