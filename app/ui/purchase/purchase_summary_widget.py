"""
Purchase Summary Widget
"""

from __future__ import annotations

from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class PurchaseSummaryWidget(QWidget):
    """
    Purchase Summary Panel
    """

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()

        self.clear()

    # -------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        frame = QFrame()

        layout = QFormLayout(frame)

        self.lbl_items = QLabel("0")

        self.lbl_qty = QLabel("0")

        self.lbl_free = QLabel("0")

        self.lbl_subtotal = QLabel("0.00")

        self.lbl_discount = QLabel("0.00")

        self.lbl_gst = QLabel("0.00")

        self.lbl_roundoff = QLabel("0.00")

        self.lbl_grand = QLabel("0.00")

        self.lbl_cost = QLabel("0.00")

        self.lbl_margin = QLabel("0.00 %")

        layout.addRow("Items", self.lbl_items)

        layout.addRow("Quantity", self.lbl_qty)

        layout.addRow("Free Qty", self.lbl_free)

        layout.addRow("Sub Total", self.lbl_subtotal)

        layout.addRow("Discount", self.lbl_discount)

        layout.addRow("GST", self.lbl_gst)

        layout.addRow("Round Off", self.lbl_roundoff)

        layout.addRow("Grand Total", self.lbl_grand)

        layout.addRow("Landing Cost", self.lbl_cost)

        layout.addRow("Margin", self.lbl_margin)

        root.addWidget(frame)

    # -------------------------------------------------

    def update_summary(

        self,

        items: int,

        qty: Decimal,

        free_qty: Decimal,

        subtotal: Decimal,

        discount: Decimal,

        gst: Decimal,

        roundoff: Decimal,

        grand: Decimal,

        landing_cost: Decimal,

        margin: Decimal,

    ):

        self.lbl_items.setText(str(items))

        self.lbl_qty.setText(str(qty))

        self.lbl_free.setText(str(free_qty))

        self.lbl_subtotal.setText(f"{subtotal:.2f}")

        self.lbl_discount.setText(f"{discount:.2f}")

        self.lbl_gst.setText(f"{gst:.2f}")

        self.lbl_roundoff.setText(f"{roundoff:.2f}")

        self.lbl_grand.setText(f"{grand:.2f}")

        self.lbl_cost.setText(f"{landing_cost:.2f}")

        self.lbl_margin.setText(f"{margin:.2f} %")

    # -------------------------------------------------

    def clear(self):

        self.update_summary(

            items=0,

            qty=Decimal("0"),

            free_qty=Decimal("0"),

            subtotal=Decimal("0"),

            discount=Decimal("0"),

            gst=Decimal("0"),

            roundoff=Decimal("0"),

            grand=Decimal("0"),

            landing_cost=Decimal("0"),

            margin=Decimal("0"),

        )