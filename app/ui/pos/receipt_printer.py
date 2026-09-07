"""
Receipt Printer
Commercial POS Version
"""

from __future__ import annotations

from datetime import datetime


class ReceiptPrinter:

    def __init__(self, settings):

        self.settings = settings

    # -------------------------------------------------

    def build_receipt(

        self,

        sale,

    ) -> str:

        lines = []

        # ------------------------------

        lines.append(
            self.settings.company_name.upper()
        )

        lines.append(
            self.settings.company_address
        )

        lines.append(
            f"GSTIN : {self.settings.gstin}"
        )

        lines.append(
            "-" * 48
        )

        lines.append(
            f"Invoice : {sale.invoice_no}"
        )

        lines.append(
            f"Date : {sale.sale_date.strftime('%d-%m-%Y %H:%M')}"
        )

        lines.append(
            f"Customer : {sale.customer_name}"
        )

        lines.append(
            "-" * 48
        )

        # ------------------------------

        lines.append(

            "{:<18}{:>5}{:>8}{:>10}".format(

                "Item",

                "Qty",

                "Rate",

                "Total",

            )

        )

        lines.append("-"*48)

        for item in sale.items:

            lines.append(

                "{:<18}{:>5}{:>8}{:>10}".format(

                    item.product_name[:18],

                    item.qty,

                    f"{item.rate:.2f}",

                    f"{item.total:.2f}",

                )

            )

        lines.append("-"*48)

        lines.append(
            f"Sub Total : {sale.sub_total:.2f}"
        )

        lines.append(
            f"Discount  : {sale.discount:.2f}"
        )

        lines.append(
            f"GST       : {sale.gst_total:.2f}"
        )

        lines.append(
            f"Grand Total : {sale.grand_total:.2f}"
        )

        lines.append(
            f"Received : {sale.received_amount:.2f}"
        )

        lines.append(
            f"Change   : {sale.change_amount:.2f}"
        )

        lines.append("-"*48)

        lines.append(
            f"Loyalty Earned : {sale.loyalty_earned}"
        )

        lines.append(
            f"Loyalty Balance : {sale.loyalty_balance}"
        )

        lines.append("-"*48)

        lines.append(
            "Thank You"
        )

        lines.append(
            "Visit Again"
        )

        lines.append(
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        return "\n".join(lines)

    # -------------------------------------------------

    def print_receipt(

        self,

        sale,

    ):

        receipt = self.build_receipt(sale)

        print(receipt)

        return receipt