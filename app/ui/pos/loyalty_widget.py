"""
Loyalty Widget
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QGroupBox,
)


class LoyaltyWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.customer = None

        self.build_ui()

        self.clear()

    # -------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        group = QGroupBox("Customer Loyalty")

        form = QFormLayout(group)

        self.lbl_name = QLabel("-")

        self.lbl_mobile = QLabel("-")

        self.lbl_points = QLabel("0")

        self.lbl_earned = QLabel("0")

        self.lbl_redeem = QLabel("0")

        self.lbl_level = QLabel("Regular")

        self.lbl_purchase = QLabel("₹0.00")

        self.lbl_next = QLabel("0")

        self.btn_redeem = QPushButton("Redeem Points")

        form.addRow("Customer", self.lbl_name)

        form.addRow("Mobile", self.lbl_mobile)

        form.addRow("Available Points", self.lbl_points)

        form.addRow("Earn This Bill", self.lbl_earned)

        form.addRow("Redeem", self.lbl_redeem)

        form.addRow("Membership", self.lbl_level)

        form.addRow("Lifetime Purchase", self.lbl_purchase)

        form.addRow("Next Reward", self.lbl_next)

        root.addWidget(group)

        root.addWidget(self.btn_redeem)

        root.addStretch()

    # -------------------------------------------------

    def load_customer(self, customer):

        self.customer = customer

        if customer is None:

            self.clear()

            return

        self.lbl_name.setText(customer.name)

        self.lbl_mobile.setText(customer.mobile)

        self.lbl_points.setText(
            str(customer.loyalty_points)
        )

        self.lbl_level.setText(
            customer.membership_level
        )

        self.lbl_purchase.setText(
            f"₹ {customer.lifetime_purchase:.2f}"
        )

    # -------------------------------------------------

    def update_bill(

        self,

        amount,

        qty,

    ):

        earn = int(

            Decimal(str(amount))

            / Decimal("100")

        )

        self.lbl_earned.setText(

            str(earn)

        )

        if self.customer:

            current = int(

                self.customer.loyalty_points

            )

            next_reward = max(

                0,

                500 - current,

            )

            self.lbl_next.setText(

                str(next_reward)

            )

    # -------------------------------------------------

    def redeem_points(

        self,

        points,

    ):

        self.lbl_redeem.setText(

            str(points)

        )

    # -------------------------------------------------

    def clear(self):

        self.lbl_name.setText("-")

        self.lbl_mobile.setText("-")

        self.lbl_points.setText("0")

        self.lbl_earned.setText("0")

        self.lbl_redeem.setText("0")

        self.lbl_level.setText("Regular")

        self.lbl_purchase.setText("₹0.00")

        self.lbl_next.setText("500")