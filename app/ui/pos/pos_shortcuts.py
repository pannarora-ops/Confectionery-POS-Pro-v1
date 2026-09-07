"""
POS Keyboard Shortcuts
Commercial POS Version
"""

from __future__ import annotations

from PySide6.QtGui import QAction, QKeySequence


class POSShortcuts:

    def __init__(self, window):

        self.window = window

        self.register()

    # -------------------------------------------------

    def register(self):

        self.add_shortcut(

            "F2",

            self.window.controller.new_bill

        )

        self.add_shortcut(

            "F3",

            self.window.controller.customer_search

        )

        self.add_shortcut(

            "F4",

            self.window.controller.hold_bill

        )

        self.add_shortcut(

            "F5",

            self.window.controller.resume_bill_dialog

        )

        self.add_shortcut(

            "F6",

            self.window.controller.payment

        )

        self.add_shortcut(

            "F7",

            self.window.controller.print_last_bill

        )

        self.add_shortcut(

            "F8",

            self.window.controller.apply_discount

        )

        self.add_shortcut(

            "F9",

            self.window.controller.scan_barcode_focus

        )

        self.add_shortcut(

            "F10",

            self.window.controller.save_bill

        )

        self.add_shortcut(

            "Ctrl+Delete",

            self.window.controller.delete_row

        )

        self.add_shortcut(

            "Ctrl+L",

            self.window.controller.loyalty_redeem

        )

        self.add_shortcut(

            "Ctrl+Q",

            self.window.close

        )

    # -------------------------------------------------

    def add_shortcut(

        self,

        key,

        callback,

    ):

        action = QAction(self.window)

        action.setShortcut(QKeySequence(key))

        action.triggered.connect(callback)

        self.window.addAction(action)