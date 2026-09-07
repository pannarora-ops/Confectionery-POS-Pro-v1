"""
Main Window.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QListWidget,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QStatusBar,
)

from app.ui.dashboard_page import DashboardPage
from app.ui.products_page import ProductsPage
from app.ui.units_page import UnitsPage
from app.ui.customers_page import CustomersPage
from app.ui.suppliers_page import SuppliersPage
from app.ui.purchase_page import PurchasePage
from app.ui.sales_page import SalesPage
from app.ui.inventory_page import InventoryPage
from app.ui.reports_page import ReportsPage
from app.ui.settings_page import SettingsPage
from app.ui.brands_page import BrandsPage

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Confectionery POS Pro")
        self.resize(1400, 850)

        self.build_ui()

    # -------------------------------------------------

    def build_ui(self):

        splitter = QSplitter()

        # ---------------- Sidebar ----------------

        self.menu = QListWidget()

        self.menu.addItems(
            [
                "Dashboard",
                "Products",
                "Brands",
                "Units",
                "Customers",
                "Suppliers",
                "Purchases",
                "Sales",
                "Inventory",
                "Reports",
                "Settings",
            ]
        )

        self.menu.setMaximumWidth(220)

        # ---------------- Pages ----------------

        self.pages = QStackedWidget()

        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(ProductsPage())
        self.pages.addWidget(BrandsPage())
        self.pages.addWidget(UnitsPage())
        self.pages.addWidget(CustomersPage())
        self.pages.addWidget(SuppliersPage())
        self.pages.addWidget(PurchasePage())
        self.pages.addWidget(SalesPage())
        self.pages.addWidget(InventoryPage())
        self.pages.addWidget(ReportsPage())
        self.pages.addWidget(SettingsPage())

        splitter.addWidget(self.menu)
        splitter.addWidget(self.pages)

        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        self.setStatusBar(QStatusBar())

        self.statusBar().showMessage("Ready")

        self.menu.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        self.menu.setCurrentRow(0)