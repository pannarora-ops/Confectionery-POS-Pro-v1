"""
Purchase Repository
Commercial POS Version
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.purchase import Purchase


class PurchaseRepository:

    def __init__(self, session: Session):
        self.session = session

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    def create(self, purchase: Purchase):

        self.session.add(purchase)
        self.session.flush()

        return purchase

    def update(self):
        self.session.flush()

    def delete(self, purchase: Purchase):
        self.session.delete(purchase)

    # -------------------------------------------------
    # Get
    # -------------------------------------------------

    def get(self, purchase_id: int):

        return (
            self.session.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

    def get_by_invoice(self, invoice_no: str):

        return (
            self.session.query(Purchase)
            .filter(Purchase.invoice_no == invoice_no)
            .first()
        )

    # -------------------------------------------------
    # Listing
    # -------------------------------------------------

    def get_all(self):

        return (
            self.session.query(Purchase)
            .order_by(Purchase.purchase_date.desc())
            .all()
        )

    # -------------------------------------------------
    # Purchase Number Generator
    # -------------------------------------------------

    def generate_purchase_no(self):

        year = datetime.now().strftime("%y")

        prefix = f"PUR{year}"

        last = (
            self.session.query(
                func.max(Purchase.id)
            ).scalar()
        )

        if not last:
            return f"{prefix}000001"

        return f"{prefix}{last + 1:06d}"

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, text: str):

        if not text:
            return self.get_all()

        text = f"%{text}%"

        return (
            self.session.query(Purchase)
            .filter(
                Purchase.invoice_no.ilike(text)
            )
            .order_by(
                Purchase.purchase_date.desc()
            )
            .all()
        )