"""
Brand Add/Edit Dialog.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from app.database.session import get_session
from app.services.brand_service import BrandService


class BrandDialog(QDialog):
    """Add/Edit Brand."""

    def __init__(self, brand=None, parent=None):
        super().__init__(parent)

        self.brand = brand

        self.session = get_session()
        self.service = BrandService(self.session)

        self.setWindowTitle(
            "Brand Master"
            if brand is None
            else "Edit Brand"
        )

        self.resize(450, 300)

        self.build_ui()

        if self.brand:
            self.load_brand()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()

        self.description = QTextEdit()
        self.description.setFixedHeight(90)

        self.active = QCheckBox("Active")
        self.active.setChecked(True)

        form.addRow("Brand Name *", self.name)
        form.addRow("Description", self.description)
        form.addRow("", self.active)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        buttons.addStretch()

        save = QPushButton("Save")
        cancel = QPushButton("Cancel")

        save.clicked.connect(self.save_brand)
        cancel.clicked.connect(self.reject)

        buttons.addWidget(save)
        buttons.addWidget(cancel)

        layout.addLayout(buttons)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load_brand(self):

        self.name.setText(
            self.brand.name
        )

        self.description.setPlainText(
            self.brand.description or ""
        )

        self.active.setChecked(
            self.brand.active
        )

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save_brand(self):

        name = self.name.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Validation",
                "Brand name is required.",
            )
            return

        try:

            if self.brand:

                self.service.update(
                    self.brand.id,
                    name=name,
                    description=self.description.toPlainText().strip(),
                    active=self.active.isChecked(),
                )

            else:

                self.service.create(
                    name=name,
                    description=self.description.toPlainText().strip(),
                )

            self.session.commit()

            self.accept()

        except Exception as exc:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )