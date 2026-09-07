"""
Login Window.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.main_window import MainWindow


class LoginWindow(QWidget):
    """Application login window."""

    def __init__(self):
        super().__init__()

        self.main_window = None

        self.setWindowTitle(
            "Confectionery POS Pro"
        )

        self.resize(420, 260)

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            "Confectionery POS Pro"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size:24px;
            font-weight:bold;
            """
        )

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Username"
        )

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        login_button = QPushButton(
            "Login"
        )

        exit_button = QPushButton(
            "Exit"
        )

        login_button.clicked.connect(
            self.login
        )

        exit_button.clicked.connect(
            self.close
        )

        layout.addStretch()

        layout.addWidget(title)

        layout.addSpacing(20)

        layout.addWidget(self.username)

        layout.addWidget(self.password)

        layout.addSpacing(15)

        layout.addWidget(login_button)

        layout.addWidget(exit_button)

        layout.addStretch()

    def login(self):
        """
        Temporary login.
        Authentication will be added later.
        """

        username = self.username.text().strip()

        password = self.password.text().strip()

        if not username:

            QMessageBox.warning(
                self,
                "Validation",
                "Username is required.",
            )

            return

        if not password:

            QMessageBox.warning(
                self,
                "Validation",
                "Password is required.",
            )

            return

        # ----------------------------------
        # Temporary Login
        # ----------------------------------

        self.main_window = MainWindow()

        self.main_window.show()

        self.close()