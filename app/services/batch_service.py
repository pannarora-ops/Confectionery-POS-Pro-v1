"""
Batch Service
Commercial POS Version
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.repositories.batch_repository import BatchRepository


class BatchService:

    def __init__(self, session: Session):

        self.session = session
        self.repo = BatchRepository(session)

    # -------------------------------------------------
    # Create / Update Batch
    # -------------------------------------------------

    def create_or_update(
        self,
        *,
        product_id: int,
        batch_no: str,
        manufacture_date: date | None,
        expiry_date: date | None,
        purchase_rate: Decimal,
        sale_rate: Decimal,
        mrp: Decimal,
        qty: Decimal,
        supplier_id: int | None = None,
        purchase_id: int | None = None,
        purchase_item_id: int | None = None,
    ) -> Batch:

        batch = self.repo.get_by_batch_no(
            product_id,
            batch_no,
        )

        if batch:

            batch.available_qty += qty

            batch.purchase_rate = purchase_rate
            batch.sale_rate = sale_rate
            batch.mrp = mrp

            if manufacture_date:
                batch.manufacture_date = manufacture_date

            if expiry_date:
                batch.expiry_date = expiry_date

            self.session.flush()

            return batch

        batch = Batch(

            product_id=product_id,

            batch_no=batch_no,

            manufacture_date=manufacture_date,

            expiry_date=expiry_date,

            purchase_rate=purchase_rate,

            sale_rate=sale_rate,

            mrp=mrp,

            available_qty=qty,

            supplier_id=supplier_id,

            purchase_id=purchase_id,

            purchase_item_id=purchase_item_id,

            active=True,
        )

        self.repo.create(batch)

        return batch

    # -------------------------------------------------
    # Batch Validation
    # -------------------------------------------------

    def validate_expiry(
        self,
        expiry_date: date | None,
    ):

        if expiry_date is None:
            return

        if expiry_date <= date.today():

            raise ValueError(
                "Batch already expired."
            )

    # -------------------------------------------------
    # Batch Closing
    # -------------------------------------------------

    def close_batch(
        self,
        batch_id: int,
    ):

        batch = self.repo.get(batch_id)

        if not batch:
            return

        if batch.available_qty > 0:

            raise ValueError(
                "Batch still contains stock."
            )

        batch.active = False

        self.session.flush()

    # -------------------------------------------------
    # FEFO Allocation
    # -------------------------------------------------

    def allocate_stock(
        self,
        product_id: int,
        qty: Decimal,
    ):

        allocations = []

        remaining = qty

        batches = self.repo.get_product_batches(
            product_id
        )

        for batch in batches:

            if remaining <= 0:
                break

            available = batch.available_qty

            if available >= remaining:

                allocations.append(

                    (
                        batch,
                        remaining,
                    )

                )

                remaining = Decimal("0")

            else:

                allocations.append(

                    (
                        batch,
                        available,
                    )

                )

                remaining -= available

        if remaining > 0:

            raise ValueError(
                "Insufficient stock."
            )

        return allocations

    # -------------------------------------------------
    # Deduct Stock
    # -------------------------------------------------

    def deduct_stock(
        self,
        batch: Batch,
        qty: Decimal,
    ):

        if batch.available_qty < qty:

            raise ValueError(
                "Batch stock not available."
            )

        batch.available_qty -= qty

        self.session.flush()

    # -------------------------------------------------
    # Add Stock
    # -------------------------------------------------

    def add_stock(
        self,
        batch: Batch,
        qty: Decimal,
    ):

        batch.available_qty += qty

        self.session.flush()

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def commit(self):

        self.session.commit()