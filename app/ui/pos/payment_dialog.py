"""
Payment Dialog
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)


class PaymentDialog(QDialog):

    def __init__(self, parent=None, total=Decimal("0")):

        super().__init__(parent)

        self.total = Decimal(str(total))

        self.setWindowTitle("Payment")

        self.resize(420, 500)

        self.build_ui()

        self.load_values()

        self.connect_signals()

    # -------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        box = QGroupBox("Payment Details")

        form = QFormLayout(box)

        self.lbl_total = QLabel()

        self.mode = QComboBox()

        self.mode.addItems([
            "Cash",
            "UPI",
            "Card",
            "Wallet",
            "Bank",
            "Credit",
            "Split Payment",
        ])

        self.cash = QDoubleSpinBox()
        self.cash.setMaximum(99999999)

        self.upi = QDoubleSpinBox()
        self.upi.setMaximum(99999999)

        self.card = QDoubleSpinBox()
        self.card.setMaximum(99999999)

        self.wallet = QDoubleSpinBox()
        self.wallet.setMaximum(99999999)

        self.bank = QDoubleSpinBox()
        self.bank.setMaximum(99999999)

        self.received = QDoubleSpinBox()
        self.received.setMaximum(99999999)

        self.change = QLabel("0.00")

        self.reference = QLineEdit()

        form.addRow("Bill Amount", self.lbl_total)
        form.addRow("Payment Mode", self.mode)
        form.addRow("Cash", self.cash)
        form.addRow("UPI", self.upi)
        form.addRow("Card", self.card)
        form.addRow("Wallet", self.wallet)
        form.addRow("Bank", self.bank)
        form.addRow("Cash Received", self.received)
        form.addRow("Change", self.change)
        form.addRow("Reference", self.reference)

        root.addWidget(box)

        buttons = QHBoxLayout()

        self.btn_ok = QPushButton("Complete Payment")

        self.btn_cancel = QPushButton("Cancel")

        buttons.addWidget(self.btn_ok)

        buttons.addWidget(self.btn_cancel)

        root.addLayout(buttons)

    # -------------------------------------------------

    def load_values(self):

        self.lbl_total.setText(
            f"₹ {self.total:.2f}"
        )

        self.cash.setValue(float(self.total))

        self.received.setValue(float(self.total))

        self.calculate_change()

    # -------------------------------------------------

    def connect_signals(self):

        self.received.valueChanged.connect(
            self.calculate_change
        )

        self.btn_ok.clicked.connect(
            self.accept_payment
        )

        self.btn_cancel.clicked.connect(
            self.reject
        )

    # -------------------------------------------------

    def calculate_change(self):

        received = Decimal(
            str(self.received.value())
        )

        change = received - self.total

        if change < 0:
            change = Decimal("0")

        self.change.setText(
            f"₹ {change:.2f}"
        )

    # -------------------------------------------------

    def payment_data(self):

        return {

            "mode": self.mode.currentText(),

            "cash": Decimal(str(self.cash.value())),

            "upi": Decimal(str(self.upi.value())),

            "card": Decimal(str(self.card.value())),

            "wallet": Decimal(str(self.wallet.value())),

            "bank": Decimal(str(self.bank.value())),

            "received": Decimal(
                str(self.received.value())
            ),

            "reference": self.reference.text(),

            "change": Decimal(
                self.change.text().replace("₹","").strip()
            )

        }

    # -------------------------------------------------

    def accept_payment(self):

        paid = (

            Decimal(str(self.cash.value()))

            + Decimal(str(self.upi.value()))

            + Decimal(str(self.card.value()))

            + Decimal(str(self.wallet.value()))

            + Decimal(str(self.bank.value()))

        )

        if paid < self.total:

            QMessageBox.warning(

                self,

                "Payment",

                "Insufficient payment."

            )

            return

        self.accept()