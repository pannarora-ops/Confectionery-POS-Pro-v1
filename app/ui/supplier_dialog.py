"""
Supplier Dialog.
"""

from PySide6.QtWidgets import (
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
from app.services.supplier_service import SupplierService


class SupplierDialog(QDialog):
    """Add/Edit Supplier Dialog."""

    def __init__(self, supplier=None, parent=None):
        super().__init__(parent)

        self.supplier = supplier

        self.session = get_session()
        self.service = SupplierService(self.session)

        self.setWindowTitle("Supplier")
        self.resize(450, 420)

        self.build_ui()

        if self.supplier:
            self.load_supplier()

    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.gst = QLineEdit()
        self.address = QTextEdit()

        form.addRow("Name", self.name)
        form.addRow("Phone", self.phone)
        form.addRow("Email", self.email)
        form.addRow("GST No.", self.gst)
        form.addRow("Address", self.address)

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

    def load_supplier(self):

        self.name.setText(self.supplier.name)
        self.phone.setText(self.supplier.phone or "")
        self.email.setText(self.supplier.email or "")
        self.gst.setText(
            getattr(
                self.supplier,
                "gst_number",
                "",
            ) or ""
        )
        self.address.setPlainText(
            self.supplier.address or ""
        )

    # -------------------------------------------------

    def save(self):

        if not self.name.text().strip():

            QMessageBox.warning(
                self,
                "Validation",
                "Supplier name is required.",
            )
            return

        data = {
            "name": self.name.text().strip(),
            "phone": self.phone.text().strip(),
            "email": self.email.text().strip(),
            "gst_number": self.gst.text().strip(),
            "address": self.address.toPlainText().strip(),
        }

        try:

            if self.supplier:

                self.service.update(
                    self.supplier.id,
                    **data,
                )

            else:

                self.service.create(
                    **data,
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