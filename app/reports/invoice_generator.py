"""
Invoice PDF Generator.
"""

from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.models.purchase import Purchase
from app.models.sale import Sale


class InvoiceGenerator:
    """Generate Sale and Purchase invoices."""

    def __init__(self, session):
        self.session = session
        self.styles = getSampleStyleSheet()

    # ----------------------------------------------------
    # Sale Invoice
    # ----------------------------------------------------

    def generate_sale_invoice(
        self,
        sale_id: int,
        output_file: str,
    ) -> None:

        sale = self.session.get(Sale, sale_id)

        if sale is None:
            raise ValueError(
                "Sale not found."
            )

        doc = SimpleDocTemplate(output_file)

        story = []

        title = self.styles["Heading1"]
        title.alignment = TA_CENTER

        story.append(
            Paragraph(
                "SALE INVOICE",
                title,
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Invoice :</b> {sale.invoice_number}",
                self.styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Date :</b> {sale.sale_date.strftime('%d-%m-%Y')}",
                self.styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Customer :</b> "
                f"{sale.customer_name or '-'}",
                self.styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        data = [
            [
                "Product",
                "Qty",
                "Rate",
                "GST %",
                "Amount",
            ]
        ]

        subtotal = Decimal("0.00")
        gst = Decimal("0.00")

        for item in sale.items:

            amount = item.quantity * item.rate

            gst_amount = (
                amount * item.gst_percent
            ) / Decimal("100")

            subtotal += amount
            gst += gst_amount

            data.append(
                [
                    item.product.name,
                    str(item.quantity),
                    f"{item.rate:.2f}",
                    f"{item.gst_percent:.2f}",
                    f"{amount:.2f}",
                ]
            )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.grey,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.beige,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 20))

        right = self.styles["Normal"]
        right.alignment = TA_RIGHT

        story.append(
            Paragraph(
                f"<b>Subtotal :</b> {subtotal:.2f}",
                right,
            )
        )

        story.append(
            Paragraph(
                f"<b>GST :</b> {gst:.2f}",
                right,
            )
        )

        story.append(
            Paragraph(
                f"<b>Grand Total :</b> "
                f"{subtotal + gst:.2f}",
                right,
            )
        )

        doc.build(story)

    # ----------------------------------------------------
    # Purchase Invoice
    # ----------------------------------------------------

    def generate_purchase_invoice(
        self,
        purchase_id: int,
        output_file: str,
    ) -> None:

        purchase = self.session.get(
            Purchase,
            purchase_id,
        )

        if purchase is None:
            raise ValueError(
                "Purchase not found."
            )

        doc = SimpleDocTemplate(output_file)

        story = []

        title = self.styles["Heading1"]
        title.alignment = TA_CENTER

        story.append(
            Paragraph(
                "PURCHASE INVOICE",
                title,
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Invoice :</b> "
                f"{purchase.invoice_number}",
                self.styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Date :</b> "
                f"{purchase.purchase_date.strftime('%d-%m-%Y')}",
                self.styles["Normal"],
            )
        )

        supplier_name = "-"

        if purchase.supplier:
            supplier_name = purchase.supplier.name

        story.append(
            Paragraph(
                f"<b>Supplier :</b> "
                f"{supplier_name}",
                self.styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        data = [
            [
                "Product",
                "Qty",
                "Rate",
                "GST %",
                "Amount",
            ]
        ]

        subtotal = Decimal("0.00")
        gst = Decimal("0.00")

        for item in purchase.items:

            amount = item.quantity * item.rate

            gst_amount = (
                amount * item.gst_percent
            ) / Decimal("100")

            subtotal += amount
            gst += gst_amount

            data.append(
                [
                    item.product.name,
                    str(item.quantity),
                    f"{item.rate:.2f}",
                    f"{item.gst_percent:.2f}",
                    f"{amount:.2f}",
                ]
            )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.darkblue,
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.whitesmoke,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 20))

        right = self.styles["Normal"]
        right.alignment = TA_RIGHT

        story.append(
            Paragraph(
                f"<b>Subtotal :</b> {subtotal:.2f}",
                right,
            )
        )

        story.append(
            Paragraph(
                f"<b>GST :</b> {gst:.2f}",
                right,
            )
        )

        story.append(
            Paragraph(
                f"<b>Total :</b> "
                f"{subtotal + gst:.2f}",
                right,
            )
        )

        doc.build(story)
        