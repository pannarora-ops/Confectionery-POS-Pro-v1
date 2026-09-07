"""
POS Table Model
"""

from __future__ import annotations

from decimal import Decimal

from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel,
)


class POSTableModel(QAbstractTableModel):

    HEADERS = [

        "Product",

        "Batch",

        "Qty",

        "Rate",

        "Disc%",

        "GST%",

        "Total",

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

        if role not in (

            Qt.DisplayRole,

            Qt.EditRole,

        ):

            return None

        row = self.rows[index.row()]

        return row[index.column()]

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

        self.rows[index.row()][index.column()] = value

        self.calculate_row(index.row())

        self.dataChanged.emit(

            index,

            index,

        )

        return True

    # -------------------------------------------------

    def add_product(

        self,

        product,

        batch,

        qty=Decimal("1"),

    ):

        self.beginInsertRows(

            QModelIndex(),

            len(self.rows),

            len(self.rows),

        )

        self.rows.append([

            product,

            batch,

            qty,

            batch.sale_rate,

            Decimal("0"),

            product.gst_percent,

            Decimal("0"),

        ])

        self.endInsertRows()

        self.calculate_row(

            len(self.rows)-1

        )

    # -------------------------------------------------

    def calculate_row(

        self,

        row_index,

    ):

        row = self.rows[row_index]

        qty = Decimal(str(row[2]))

        rate = Decimal(str(row[3]))

        discount = Decimal(str(row[4]))

        gst = Decimal(str(row[5]))

        gross = qty * rate

        discount_amt = (

            gross * discount

        ) / Decimal("100")

        taxable = gross - discount_amt

        gst_amt = (

            taxable * gst

        ) / Decimal("100")

        total = taxable + gst_amt

        row[6] = round(total,2)

    # -------------------------------------------------

    def subtotal(self):

        total = Decimal("0")

        for row in self.rows:

            total += Decimal(str(row[6]))

        return total

    # -------------------------------------------------

    def total_qty(self):

        qty = Decimal("0")

        for row in self.rows:

            qty += Decimal(str(row[2]))

        return qty

    # -------------------------------------------------

    def remove_row(

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

    def clear(self):

        self.beginResetModel()

        self.rows.clear()

        self.endResetModel()

    # -------------------------------------------------

    def export(self):

        result = []

        for row in self.rows:

            result.append({

                "product":row[0],

                "batch":row[1],

                "qty":row[2],

                "rate":row[3],

                "discount":row[4],

                "gst":row[5],

                "total":row[6],

            })

        return result