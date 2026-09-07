"""
Dashboard Page.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.database.session import get_session
from app.services.dashboard_service import DashboardService


class DashboardPage(QWidget):
    """Dashboard Page."""

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.dashboard = DashboardService(self.session)

        self.build_ui()

    def create_card(
        self,
        title: str,
        value: str,
    ) -> QFrame:
        """Create dashboard card."""

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        frame.setStyleSheet("""
        QFrame{
            border:1px solid #444;
            border-radius:10px;
            background:#2b2b2b;
        }
        """)

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size:18px;
            color:white;
        """)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            font-size:40px;
            font-weight:bold;
            color:#2E86DE;
        """)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)
        layout.addStretch()

        return frame

    def build_ui(self):
        """Build dashboard."""

        summary = self.dashboard.summary()

        layout = QGridLayout(self)
        layout.setSpacing(15)

        # Today's Sales
        layout.addWidget(
            self.create_card(
                "Today's Sales",
                f"₹ {summary['today_sales']:,.2f}",
            ),
            0,
            0,
        )

        # Sales Count
        layout.addWidget(
            self.create_card(
                "Sales Count",
                str(summary["today_sale_count"]),
            ),
            0,
            1,
        )

        # Purchase Count
        layout.addWidget(
            self.create_card(
                "Purchase Count",
                str(summary["today_purchase_count"]),
            ),
            0,
            2,
        )

        # Products
        layout.addWidget(
            self.create_card(
                "Products",
                str(summary["products"]),
            ),
            1,
            0,
        )

        # Customers
        layout.addWidget(
            self.create_card(
                "Customers",
                str(summary["customers"]),
            ),
            1,
            1,
        )

        # Suppliers
        layout.addWidget(
            self.create_card(
                "Suppliers",
                str(summary["suppliers"]),
            ),
            1,
            2,
        )

        # Stock Quantity
        layout.addWidget(
            self.create_card(
                "Stock Qty",
                f"{summary['stock_quantity']:,.3f}",
            ),
            2,
            0,
        )

        # Stock Value
        layout.addWidget(
            self.create_card(
                "Stock Value",
                f"₹ {summary['stock_value']:,.2f}",
            ),
            2,
            1,
            1,
            2,
        )