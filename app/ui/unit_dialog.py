"""
Unit Dialog.
"""

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.database.session import get_session
from app.services.unit_service import UnitService


class UnitDialog(QDialog):
    """Add/Edit Unit Dialog."""

    def __init__(self, unit=None, parent=None):
        super().__init__(parent)

        self.unit = unit

        self.session = get_session()
        self.service = UnitService(self.session)

        self.setWindowTitle("Unit")
        self.resize(420, 220)

        self.build_ui()

        if self.unit:
            self.load_unit()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()

        self.short_name = QLineEdit()

        self.active = QCheckBox("Active")
        self.active.setChecked(True)

        form.addRow("Unit Name", self.name)
        form.addRow("Short Name", self.short_name)
        form.addRow("", self.active)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        save = QPushButton("Save")
        cancel = QPushButton("Cancel")

        save.clicked.connect(self.save)
        cancel.clicked.connect(self.reject)

        buttons.addStretch()
        buttons.addWidget(save)
        buttons.addWidget(cancel)

        layout.addLayout(buttons)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load_unit(self):

        self.name.setText(self.unit.name)
        self.short_name.setText(self.unit.short_name)
        self.active.setChecked(self.unit.active)

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save(self):

        name = self.name.text().strip()
        short_name = self.short_name.text().strip()
        active = self.active.isChecked()

        if not name:

            QMessageBox.warning(
                self,
                "Validation",
                "Unit Name is required.",
            )

            return

        if not short_name:

            QMessageBox.warning(
                self,
                "Validation",
                "Short Name is required.",
            )

            return

        try:

            if self.unit:

                self.service.update_unit(
                    unit_id=self.unit.id,
                    name=name,
                    short_name=short_name,
                    active=active,
                )

            else:

                self.service.create_unit(
                    name=name,
                    short_name=short_name,
                    active=active,
                )

            self.accept()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )