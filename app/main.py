"""
Application Entry Point.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.ui.login_window import LoginWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setApplicationName(
        "Confectionery POS Pro"
    )

    window = LoginWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())