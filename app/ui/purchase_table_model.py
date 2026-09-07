"""
Purchase Table Model
"""

from __future__ import annotations

from decimal import Decimal

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
)


class PurchaseTableModel(QAbstractTableModel):

    HEADERS = [

        "Product",

        "Batch",

        "Expiry",

        "Qty",

        "Free",

        "P.Rate",

        "Disc %",

        "GST %",

        "MRP",

        "Sale",

        "Amount",

    ]

    def __init__(self):

        super().__init__()

        self.rows = []

    # -------------------------------------------------

    def rowCount(self, parent=QModelIndex()):

        return len(self.rows)

    # -------------------------------------------------

    def columnCount(self, parent=QModelIndex()):

        return len(self.HEADERS)

    # -------------------------------------------------

    def headerData(

        self,

        section,

        orientation,

        role,

    ):

        if role != Qt.DisplayRole:

            return None

        if orientation == Qt.Horizontal:

            return self.HEADERS[section]

        return str(section + 1)

    # -------------------------------------------------

    def data(

        self,

        index,

        role,

    ):

        if not index.isValid():

            return None

        row = self.rows[index.row()]

        col = index.column()

        if role in (

            Qt.DisplayRole,

            Qt.EditRole,

        ):

            return row[col]

        return None

    # -------------------------------------------------

    def flags(self, index):

        return (

            Qt.ItemIsSelectable

            | Qt.ItemIsEnabled

            | Qt.ItemIsEditable

        )

    # -------------------------------------------------

    def setData(

        self,

        index,

        value,

        role,

    ):

        if role != Qt.EditRole:

            return False

        row = self.rows[index.row()]

        row[index.column()] = value

        self.calculate_row(index.row())

        self.dataChanged.emit(

            index,

            index,

        )

        return True

    # -------------------------------------------------

    def add_item(self):

        self.beginInsertRows(

            QModelIndex(),

            len(self.rows),

            len(self.rows),

        )

        self.rows.append(

            [

                "",                 # Product

                "",                 # Batch

                "",                 # Expiry

                Decimal("1"),       # Qty

                Decimal("0"),       # Free

                Decimal("0"),       # Purchase

                Decimal("0"),       # Discount

                Decimal("0"),       # GST

                Decimal("0"),       # MRP

                Decimal("0"),       # Sale

                Decimal("0"),       # Amount

            ]

        )

        self.endInsertRows()

    # -------------------------------------------------

    def remove_item(

        self,

        row,

    ):

        if row < 0:

            return

        self.beginRemoveRows(

            QModelIndex(),

            row,

            row,

        )

        self.rows.pop(row)

        self.endRemoveRows()

    # -------------------------------------------------

    def calculate_row(

        self,

        row_index,

    ):

        row = self.rows[row_index]

        qty = Decimal(str(row[3]))

        rate = Decimal(str(row[5]))

        disc = Decimal(str(row[6]))

        gst = Decimal(str(row[7]))

        gross = qty * rate

        discount = gross * disc / Decimal("100")

        taxable = gross - discount

        gst_amount = taxable * gst / Decimal("100")

        total = taxable + gst_amount

        row[10] = round(total, 2)

    # -------------------------------------------------

    def clear(self):

        self.beginResetModel()

        self.rows.clear()

        self.endResetModel()

    # -------------------------------------------------

    def subtotal(self):

        total = Decimal("0")

        for row in self.rows:

            total += Decimal(str(row[10]))

        return round(total, 2)

    # -------------------------------------------------

    def total_qty(self):

        qty = Decimal("0")

        for row in self.rows:

            qty += Decimal(str(row[3]))

            qty += Decimal(str(row[4]))

        return qty

    # -------------------------------------------------

    def export(self):

        data = []

        for row in self.rows:

            data.append({

                "product": row[0],

                "batch": row[1],

                "expiry": row[2],

                "qty": Decimal(str(row[3])),

                "free_qty": Decimal(str(row[4])),

                "purchase_rate": Decimal(str(row[5])),

                "discount": Decimal(str(row[6])),

                "gst": Decimal(str(row[7])),

                "mrp": Decimal(str(row[8])),

                "sale_rate": Decimal(str(row[9])),

                "total": Decimal(str(row[10])),

            })

        return data