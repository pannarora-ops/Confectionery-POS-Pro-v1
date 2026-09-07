"""
Batch Repository
Commercial POS Version
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.batch import Batch


class BatchRepository:

    def __init__(self, session: Session):

        self.session = session

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    def create(self, batch: Batch):

        self.session.add(batch)
        self.session.flush()

        return batch

    def update(self):

        self.session.flush()

    def delete(self, batch: Batch):

        self.session.delete(batch)

    # -------------------------------------------------
    # Get
    # -------------------------------------------------

    def get(self, batch_id: int):

        return (
            self.session.query(Batch)
            .filter(Batch.id == batch_id)
            .first()
        )

    def get_by_batch_no(
        self,
        product_id: int,
        batch_no: str,
    ):

        return (
            self.session.query(Batch)
            .filter(
                Batch.product_id == product_id,
                Batch.batch_no == batch_no,
            )
            .first()
        )

    # -------------------------------------------------
    # Product Batches
    # -------------------------------------------------

    def get_product_batches(
        self,
        product_id: int,
    ):

        return (
            self.session.query(Batch)
            .filter(
                Batch.product_id == product_id,
                Batch.available_qty > 0,
                Batch.active.is_(True),
            )
            .order_by(
                Batch.expiry_date.asc()
            )
            .all()
        )

    # -------------------------------------------------
    # FEFO
    # -------------------------------------------------

    def get_fefo_batch(
        self,
        product_id: int,
    ):

        return (
            self.session.query(Batch)
            .filter(
                Batch.product_id == product_id,
                Batch.available_qty > 0,
                Batch.active.is_(True),
            )
            .order_by(
                Batch.expiry_date.asc(),
                Batch.id.asc(),
            )
            .first()
        )

    # -------------------------------------------------
    # Expired
    # -------------------------------------------------

    def expired_batches(self):

        today = date.today()

        return (
            self.session.query(Batch)
            .filter(
                Batch.expiry_date < today,
                Batch.available_qty > 0,
            )
            .order_by(
                Batch.expiry_date
            )
            .all()
        )

    # -------------------------------------------------
    # Near Expiry
    # -------------------------------------------------

    def near_expiry(
        self,
        days: int = 30,
    ):

        today = date.today()

        limit = today + timedelta(days=days)

        return (
            self.session.query(Batch)
            .filter(
                Batch.expiry_date >= today,
                Batch.expiry_date <= limit,
                Batch.available_qty > 0,
            )
            .order_by(
                Batch.expiry_date
            )
            .all()
        )

    # -------------------------------------------------
    # Low Batch Stock
    # -------------------------------------------------

    def low_stock_batches(self):

        return (
            self.session.query(Batch)
            .filter(
                Batch.available_qty <= 0,
                Batch.active.is_(True),
            )
            .all()
        )

    # -------------------------------------------------
    # Active
    # -------------------------------------------------

    def active_batches(self):

        return (
            self.session.query(Batch)
            .filter(
                Batch.active.is_(True)
            )
            .all()
        )