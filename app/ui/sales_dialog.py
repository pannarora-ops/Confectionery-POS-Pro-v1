"""
Sales Page.
"""

from PySide6.QtWidgets import QWidget
from app.database.session import get_session
from app.services.report_service import ReportService
from app.ui.sales_dialog import SalesDialog


class SalesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.session = get_session()
        self.report = ReportService(self.session)

        self.build_ui()
        self.load_sales()