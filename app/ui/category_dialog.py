"""
Category Add/Edit Dialog.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)

from app.database.session import get_session
from app.services.category_service import CategoryService


class CategoryDialog(QDialog):
    """Category Dialog."""

    def __init__(self, category=None, parent=None):
        super().__init__(parent)

        self.category = category

        self.session = get_session()
        self.service = CategoryService(self.session)

        self.setWindowTitle(
            "Add Category"
            if category is None
            else "Edit Category"
        )

        self.resize(420, 220)

        self.build_ui()

        if self.category:
            self.load_category()

    # ------------------------------------
    # UI
    # ------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()

        self.description = QTextEdit()
        self.description.setFixedHeight(90)

        form.addRow("Category Name", self.name)
        form.addRow("Description", self.description)

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

    # ------------------------------------
    # Load
    # ------------------------------------

    def load_category(self):

        self.name.setText(
            self.category.name
        )

        self.description.setPlainText(
            self.category.description or ""
        )

    # ------------------------------------
    # Save
    # ------------------------------------

    def save(self):

        name = self.name.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Validation",
                "Category name required.",
            )

            return

        description = (
            self.description
            .toPlainText()
            .strip()
        )

        try:

            if self.category:

                self.service.update(
                    self.category.id,
                    name=name,
                    description=description,
                )

            else:

                self.service.create(
                    name=name,
                    description=description,
                )

            self.accept()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )