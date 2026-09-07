"""
Purchase Calculation Engine
"""

from __future__ import annotations

from decimal import Decimal


class PurchaseCalculator:

    @staticmethod
    def calculate_item(
        qty: Decimal,
        free_qty: Decimal,
        purchase_rate: Decimal,
        discount_percent: Decimal,
        gst_percent: Decimal,
        gst_type: str,
    ):

        gross = qty * purchase_rate

        discount_amount = (
            gross * discount_percent
        ) / Decimal("100")

        taxable = gross - discount_amount

        gst_amount = (
            taxable * gst_percent
        ) / Decimal("100")

        if gst_type == "Inclusive":

            taxable = (
                taxable * Decimal("100")
            ) / (
                Decimal("100") + gst_percent
            )

            gst_amount = gross - taxable

        total = taxable + gst_amount

        total_qty = qty + free_qty

        landing_cost = Decimal("0")

        if total_qty > 0:

            landing_cost = (
                total / total_qty
            )

        return {

            "gross": gross,

            "discount": discount_amount,

            "taxable": taxable,

            "gst_amount": gst_amount,

            "total": total,

            "landing_cost": landing_cost,

        }