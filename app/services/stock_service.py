"""
Stock Service
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.stock_transaction import StockTransaction


class StockService:

    def __init__(self, session: Session):

        self.session = session

    # -------------------------------------------------
    # Current Stock
    # -------------------------------------------------

    def current_stock(
        self,
        product_id: int,
    ) -> Decimal:

        qty = (
            self.session.query(
                func.coalesce(
                    func.sum(
                        Batch.available_qty
                    ),
                    0,
                )
            )
            .filter(
                Batch.product_id == product_id,
                Batch.active.is_(True),
            )
            .scalar()
        )

        return Decimal(str(qty))

    # -------------------------------------------------
    # Batch Stock
    # -------------------------------------------------

    def batch_stock(
        self,
        batch_id: int,
    ) -> Decimal:

        batch = (
            self.session.query(Batch)
            .filter(Batch.id == batch_id)
            .first()
        )

        if not batch:
            return Decimal("0")

        return Decimal(str(batch.available_qty))

    # -------------------------------------------------
    # Purchase Entry
    # -------------------------------------------------

    def purchase_stock(
        self,
        product_id: int,
        batch_id: int,
        qty: Decimal,
        bill_no: str,
    ):

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch_id,

            transaction_type="PURCHASE",

            quantity=qty,

            reference_type="PURCHASE",

            reference_no=bill_no,

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Sale Entry
    # -------------------------------------------------

    def sale_stock(
        self,
        product_id: int,
        batch_id: int,
        qty: Decimal,
        invoice_no: str,
    ):

        batch = (
            self.session.query(Batch)
            .filter(
                Batch.id == batch_id
            )
            .first()
        )

        if batch is None:
            raise ValueError(
                "Batch not found."
            )

        if batch.available_qty < qty:

            raise ValueError(
                "Insufficient batch stock."
            )

        batch.available_qty -= qty

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch.id,

            quantity=-qty,

            transaction_type="SALE",

            reference_type="SALE",

            reference_no=invoice_no,

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Purchase Return
    # -------------------------------------------------

    def purchase_return(

        self,

        product_id: int,

        batch_id: int,

        qty: Decimal,

        bill_no: str,

    ):

        batch = (
            self.session.query(Batch)
            .filter(
                Batch.id == batch_id
            )
            .first()
        )

        batch.available_qty -= qty

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch.id,

            quantity=-qty,

            transaction_type="PURCHASE_RETURN",

            reference_type="PURCHASE_RETURN",

            reference_no=bill_no,

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Sales Return
    # -------------------------------------------------

    def sales_return(

        self,

        product_id: int,

        batch_id: int,

        qty: Decimal,

        invoice_no: str,

    ):

        batch = (
            self.session.query(Batch)
            .filter(
                Batch.id == batch_id
            )
            .first()
        )

        batch.available_qty += qty

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch.id,

            quantity=qty,

            transaction_type="SALE_RETURN",

            reference_type="SALE_RETURN",

            reference_no=invoice_no,

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Damage
    # -------------------------------------------------

    def damage(

        self,

        product_id: int,

        batch_id: int,

        qty: Decimal,

        remarks: str,

    ):

        batch = (
            self.session.query(Batch)
            .filter(
                Batch.id == batch_id
            )
            .first()
        )

        batch.available_qty -= qty

        batch.damaged_qty += qty

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch.id,

            quantity=-qty,

            transaction_type="DAMAGE",

            remarks=remarks,

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Expired
    # -------------------------------------------------

    def expired(

        self,

        product_id: int,

        batch_id: int,

        qty: Decimal,

    ):

        batch = (
            self.session.query(Batch)
            .filter(
                Batch.id == batch_id
            )
            .first()
        )

        batch.available_qty -= qty

        batch.expired_qty += qty

        trx = StockTransaction(

            product_id=product_id,

            batch_id=batch.id,

            quantity=-qty,

            transaction_type="EXPIRED",

        )

        self.session.add(trx)

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def commit(self):

        self.session.commit()