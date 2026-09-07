"""
Categories Page.
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
from app.services.category_service import CategoryService
from app.ui.category_dialog import CategoryDialog


class CategoriesPage(QWidget):
    """Categories Management."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = CategoryService(self.session)

        self.build_ui()
        self.load_categories()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Categories")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        # Toolbar

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search category..."
        )

        self.search.textChanged.connect(
            self.search_category
        )

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(self.add_category)
        edit_btn.clicked.connect(self.edit_category)
        delete_btn.clicked.connect(self.delete_category)
        refresh_btn.clicked.connect(
            self.load_categories
        )

        toolbar.addWidget(self.search)
        toolbar.addStretch()
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # Table

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Category",
                "Description",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.doubleClicked.connect(
            self.edit_category
        )

        layout.addWidget(self.table)

        self.status = QLabel()
        layout.addWidget(self.status)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load_categories(self):

        categories = self.service.get_all()

        self.table.setRowCount(
            len(categories)
        )

        for row, category in enumerate(categories):

            values = [
                category.id,
                category.name,
                category.description or "",
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
            f"Total Categories : {len(categories)}"
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search_category(self):

        text = self.search.text().lower()

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
    # Selected Category
    # -------------------------------------------------

    def selected_category(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        category_id = int(
            self.table.item(row, 0).text()
        )

        return self.service.get(category_id)

    # -------------------------------------------------
    # Add
    # -------------------------------------------------

    def add_category(self):

        dialog = CategoryDialog(parent=self)

        if dialog.exec():
            self.load_categories()

    # -------------------------------------------------
    # Edit
    # -------------------------------------------------

    def edit_category(self):

        category = self.selected_category()

        if category is None:

            QMessageBox.warning(
                self,
                "Category",
                "Please select a category.",
            )

            return

        dialog = CategoryDialog(
            category=category,
            parent=self,
        )

        if dialog.exec():

            self.load_categories()

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_category(self):

        category = self.selected_category()

        if category is None:

            QMessageBox.warning(
                self,
                "Category",
                "Please select a category.",
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Category",
            f"Delete '{category.name}' ?",
            QMessageBox.Yes
            | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete(
                category.id
            )

            self.load_categories()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )