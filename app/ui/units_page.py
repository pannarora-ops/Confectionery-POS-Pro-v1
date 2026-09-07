"""
Units Page.
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
from app.services.unit_service import UnitService
from app.ui.unit_dialog import UnitDialog


class UnitsPage(QWidget):
    """Unit Master Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.service = UnitService(self.session)

        self.build_ui()
        self.load_units()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Unit Master")
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)
        layout.addWidget(title)

        # ---------------- Toolbar ----------------

        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Unit...")
        self.search.textChanged.connect(self.search_units)

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(self.add_unit)
        edit_btn.clicked.connect(self.edit_unit)
        delete_btn.clicked.connect(self.delete_unit)
        refresh_btn.clicked.connect(self.load_units)

        toolbar.addWidget(self.search)
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # ---------------- Table ----------------

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Unit",
            "Short Name",
            "Status",
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.doubleClicked.connect(
            self.edit_unit
        )

        layout.addWidget(self.table)

        self.status = QLabel()

        layout.addWidget(self.status)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load_units(self):

        units = self.service.get_all()

        self.table.setRowCount(len(units))

        for row, unit in enumerate(units):

            values = [
                unit.id,
                unit.name,
                unit.short_name,
                "Active" if unit.active else "Inactive",
            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                if col == 0:
                    item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(
                    row,
                    col,
                    item,
                )

        self.status.setText(
            f"Total Units : {len(units)}"
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search_units(self):

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

    # -------------------------------------------------
    # Selected
    # -------------------------------------------------

    def selected_unit_id(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return int(
            self.table.item(row, 0).text()
        )

    # -------------------------------------------------
    # Add
    # -------------------------------------------------

    def add_unit(self):

        dialog = UnitDialog(parent=self)

        if dialog.exec():
            self.load_units()

    # -------------------------------------------------
    # Edit
    # -------------------------------------------------

    def edit_unit(self):

        unit_id = self.selected_unit_id()

        if unit_id is None:

            QMessageBox.warning(
                self,
                "Units",
                "Please select a unit.",
            )

            return

        unit = self.service.get(unit_id)

        if unit is None:

            QMessageBox.warning(
                self,
                "Units",
                "Unit not found.",
            )

            return

        dialog = UnitDialog(
            unit=unit,
            parent=self,
        )

        if dialog.exec():
            self.load_units()

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_unit(self):

        unit_id = self.selected_unit_id()

        if unit_id is None:

            QMessageBox.warning(
                self,
                "Units",
                "Please select a unit.",
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Unit",
            "Delete selected unit?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            self.service.delete_unit(unit_id)

            self.load_units()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )