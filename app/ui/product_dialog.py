"""
Advanced Product Dialog.
"""

from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from app.database.session import get_session

from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.brand_service import BrandService
from app.services.unit_service import UnitService


class ProductDialog(QDialog):
    """Advanced Product Dialog."""

    def __init__(self, product=None, parent=None):

        super().__init__(parent)

        self.product = product
        self.image_path = None

        self.session = get_session()

        self.product_service = ProductService(
            self.session
        )

        self.category_service = CategoryService(
            self.session
        )

        self.brand_service = BrandService(
            self.session
        )

        self.unit_service = UnitService(
            self.session
        )

        self.setWindowTitle("Product Master")

        self.resize(850, 700)

        self.build_ui()

        self.load_categories()
        self.load_brands()
        self.load_units()

        if self.product:
            self.load_product()
        else:
            self.product_no.setText(
                self.product_service.generate_product_no()
            )

    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        # ============================================
        # Basic Information
        # ============================================

        basic = QGroupBox("Basic Information")

        basic_layout = QGridLayout()

        self.product_no = QLineEdit()
        self.product_no.setReadOnly(True)

        self.sku = QLineEdit()

        self.barcode = QLineEdit()

        self.manufacturer_serial = QLineEdit()

        self.name = QLineEdit()

        self.description = QTextEdit()
        self.description.setFixedHeight(70)

        self.hsn = QLineEdit()

        basic_layout.addWidget(
            QLabel("Product No."),
            0,
            0,
        )
        basic_layout.addWidget(
            self.product_no,
            0,
            1,
        )

        basic_layout.addWidget(
            QLabel("SKU"),
            0,
            2,
        )
        basic_layout.addWidget(
            self.sku,
            0,
            3,
        )

        basic_layout.addWidget(
            QLabel("Barcode"),
            1,
            0,
        )
        basic_layout.addWidget(
            self.barcode,
            1,
            1,
        )

        basic_layout.addWidget(
            QLabel("Manufacturer Serial"),
            1,
            2,
        )
        basic_layout.addWidget(
            self.manufacturer_serial,
            1,
            3,
        )

        basic_layout.addWidget(
            QLabel("Product Name"),
            2,
            0,
        )
        basic_layout.addWidget(
            self.name,
            2,
            1,
            1,
            3,
        )

        basic_layout.addWidget(
            QLabel("HSN Code"),
            3,
            0,
        )
        basic_layout.addWidget(
            self.hsn,
            3,
            1,
        )

        basic_layout.addWidget(
            QLabel("Description"),
            4,
            0,
        )
        basic_layout.addWidget(
            self.description,
            4,
            1,
            1,
            3,
        )

        basic.setLayout(basic_layout)

        layout.addWidget(basic)

        # ============================================
        # Category & Brand
        # ============================================

        master = QGroupBox("Category & Brand")

        form = QFormLayout()

        self.category = QComboBox()

        self.brand = QComboBox()

        self.add_category = QPushButton("+")
        self.add_brand = QPushButton("+")

        cat_layout = QHBoxLayout()
        cat_layout.addWidget(self.category)
        cat_layout.addWidget(self.add_category)

        brand_layout = QHBoxLayout()
        brand_layout.addWidget(self.brand)
        brand_layout.addWidget(self.add_brand)

        form.addRow(
            "Category",
            cat_layout,
        )

        form.addRow(
            "Brand",
            brand_layout,
        )

        master.setLayout(form)

        layout.addWidget(master)

        # ============================================
        # Pricing
        # ============================================

        pricing = QGroupBox("Pricing")

        grid = QGridLayout()

        self.purchase_price = QDoubleSpinBox()
        self.purchase_price.setMaximum(
            9999999
        )
        self.purchase_price.setDecimals(2)

        self.selling_price = QDoubleSpinBox()
        self.selling_price.setMaximum(
            9999999
        )
        self.selling_price.setDecimals(2)

        self.mrp = QDoubleSpinBox()
        self.mrp.setMaximum(
            9999999
        )
        self.mrp.setDecimals(2)

        self.gst = QComboBox()

        for value in [
            "0",
            "3",
            "5",
            "12",
            "18",
            "28",
        ]:
            self.gst.addItem(value)

        self.gst_type = QComboBox()

        self.gst_type.addItems(
            [
                "Exclusive",
                "Inclusive",
            ]
        )

        grid.addWidget(
            QLabel("Purchase Price"),
            0,
            0,
        )
        grid.addWidget(
            self.purchase_price,
            0,
            1,
        )

        grid.addWidget(
            QLabel("Selling Price"),
            0,
            2,
        )
        grid.addWidget(
            self.selling_price,
            0,
            3,
        )

        grid.addWidget(
            QLabel("MRP"),
            1,
            0,
        )
        grid.addWidget(
            self.mrp,
            1,
            1,
        )

        grid.addWidget(
            QLabel("GST %"),
            1,
            2,
        )
        grid.addWidget(
            self.gst,
            1,
            3,
        )

        grid.addWidget(
            QLabel("GST Type"),
            2,
            0,
        )
        grid.addWidget(
            self.gst_type,
            2,
            1,
        )

        pricing.setLayout(grid)

        layout.addWidget(pricing)
                # ============================================
        # Units
        # ============================================

        unit_group = QGroupBox("Units")

        unit_grid = QGridLayout()

        self.primary_unit = QComboBox()
        self.secondary_unit = QComboBox()

        self.add_unit = QPushButton("+")

        self.conversion = QDoubleSpinBox()
        self.conversion.setDecimals(4)
        self.conversion.setMaximum(999999)
        self.conversion.setValue(1)

        unit_layout = QHBoxLayout()
        unit_layout.addWidget(self.secondary_unit)
        unit_layout.addWidget(self.add_unit)

        unit_grid.addWidget(
            QLabel("Primary Unit"),
            0,
            0,
        )

        unit_grid.addWidget(
            self.primary_unit,
            0,
            1,
        )

        unit_grid.addWidget(
            QLabel("Secondary Unit"),
            1,
            0,
        )

        unit_grid.addLayout(
            unit_layout,
            1,
            1,
        )

        unit_grid.addWidget(
            QLabel("Conversion"),
            2,
            0,
        )

        unit_grid.addWidget(
            self.conversion,
            2,
            1,
        )

        self.conversion_note = QLabel(
            "Example : 1 Box = 12 PCS"
        )

        self.conversion_note.setStyleSheet(
            "color:gray;"
        )

        unit_grid.addWidget(
            self.conversion_note,
            3,
            0,
            1,
            2,
        )

        unit_group.setLayout(unit_grid)

        layout.addWidget(unit_group)

        # ============================================
        # Stock Information
        # ============================================

        stock_group = QGroupBox(
            "Stock Information"
        )

        stock_grid = QGridLayout()

        self.opening_stock = QDoubleSpinBox()
        self.opening_stock.setDecimals(3)
        self.opening_stock.setMaximum(999999)

        self.minimum_stock = QSpinBox()
        self.minimum_stock.setMaximum(999999)

        self.maximum_stock = QSpinBox()
        self.maximum_stock.setMaximum(999999)

        self.reorder_level = QSpinBox()
        self.reorder_level.setMaximum(999999)

        stock_grid.addWidget(
            QLabel("Opening Stock"),
            0,
            0,
        )

        stock_grid.addWidget(
            self.opening_stock,
            0,
            1,
        )

        stock_grid.addWidget(
            QLabel("Minimum Stock"),
            0,
            2,
        )

        stock_grid.addWidget(
            self.minimum_stock,
            0,
            3,
        )

        stock_grid.addWidget(
            QLabel("Maximum Stock"),
            1,
            0,
        )

        stock_grid.addWidget(
            self.maximum_stock,
            1,
            1,
        )

        stock_grid.addWidget(
            QLabel("Reorder Level"),
            1,
            2,
        )

        stock_grid.addWidget(
            self.reorder_level,
            1,
            3,
        )

        stock_group.setLayout(
            stock_grid
        )

        layout.addWidget(
            stock_group
        )

        # ============================================
        # Product Image
        # ============================================

        image_group = QGroupBox(
            "Product Image"
        )

        image_layout = QHBoxLayout()

        self.image_label = QLabel(
            "No Image Selected"
        )

        self.image_button = QPushButton(
            "Browse..."
        )

        self.image_button.clicked.connect(
            self.select_image
        )

        image_layout.addWidget(
            self.image_label
        )

        image_layout.addStretch()

        image_layout.addWidget(
            self.image_button
        )

        image_group.setLayout(
            image_layout
        )

        layout.addWidget(
            image_group
        )

        # ============================================
        # Buttons
        # ============================================

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.save_button = QPushButton(
            "Save"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.save_button.clicked.connect(
            self.save
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        buttons.addWidget(
            self.save_button
        )

        buttons.addWidget(
            self.cancel_button
        )

        layout.addLayout(
            buttons
        )
            # -------------------------------------------------
    # Load Categories
    # -------------------------------------------------

    def load_categories(self):

        self.category.clear()

        categories = self.category_service.get_all()

        for category in categories:

            self.category.addItem(
                category.name,
                category.id,
            )

    # -------------------------------------------------
    # Load Brands
    # -------------------------------------------------

    def load_brands(self):

        self.brand.clear()

        self.brand.addItem(
            "-- Select Brand --",
            None,
        )

        brands = self.brand_service.get_all()

        for brand in brands:

            self.brand.addItem(
                brand.name,
                brand.id,
            )

    # -------------------------------------------------
    # Load Units
    # -------------------------------------------------

    def load_units(self):

        self.primary_unit.clear()
        self.secondary_unit.clear()

        units = self.unit_service.get_all()

        for unit in units:

            self.primary_unit.addItem(
                unit.name,
                unit.id,
            )

            self.secondary_unit.addItem(
                unit.name,
                unit.id,
            )

    # -------------------------------------------------
    # Load Product
    # -------------------------------------------------

    def load_product(self):

        p = self.product

        self.product_no.setText(p.product_no)
        self.sku.setText(p.sku)
        self.barcode.setText(p.barcode or "")
        self.manufacturer_serial.setText(
            p.manufacturer_serial_no or ""
        )

        self.name.setText(p.name)

        self.description.setPlainText(
            p.description or ""
        )

        self.hsn.setText(
            p.hsn_code or ""
        )

        self.purchase_price.setValue(
            float(p.purchase_price)
        )

        self.selling_price.setValue(
            float(p.selling_price)
        )

        self.mrp.setValue(
            float(p.mrp)
        )

        self.gst.setCurrentText(
            str(p.gst_percent)
        )

        self.gst_type.setCurrentText(
            p.gst_type
        )

        self.conversion.setValue(
            p.conversion_factor
        )

        self.opening_stock.setValue(
            p.opening_stock
        )

        self.minimum_stock.setValue(
            p.minimum_stock
        )

        self.maximum_stock.setValue(
            p.maximum_stock
        )

        self.reorder_level.setValue(
            p.reorder_level
        )

        # Category

        index = self.category.findData(
            p.category_id
        )

        if index >= 0:
            self.category.setCurrentIndex(index)

        # Brand

        index = self.brand.findData(
            p.brand_id
        )

        if index >= 0:
            self.brand.setCurrentIndex(index)

        # Primary Unit

        index = self.primary_unit.findData(
            p.primary_unit_id
        )

        if index >= 0:
            self.primary_unit.setCurrentIndex(index)

        # Secondary Unit

        index = self.secondary_unit.findData(
            p.secondary_unit_id
        )

        if index >= 0:
            self.secondary_unit.setCurrentIndex(index)

        if p.image_path:

            self.image_path = p.image_path

            self.image_label.setText(
                p.image_path
            )

    # -------------------------------------------------
    # Select Image
    # -------------------------------------------------

    def select_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)",
        )

        if filename:

            self.image_path = filename

            self.image_label.setText(
                filename
            )

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save(self):

        if not self.name.text().strip():

            QMessageBox.warning(
                self,
                "Validation",
                "Product name required.",
            )

            return

        data = {

            "sku":
                self.sku.text().strip(),

            "barcode":
                self.barcode.text().strip(),

            "manufacturer_serial_no":
                self.manufacturer_serial.text().strip(),

            "name":
                self.name.text().strip(),

            "description":
                self.description.toPlainText().strip(),

            "hsn_code":
                self.hsn.text().strip(),

            "category_id":
                self.category.currentData(),

            "brand_id":
                self.brand.currentData(),

            "purchase_price":
                Decimal(
                    str(
                        self.purchase_price.value()
                    )
                ),

            "selling_price":
                Decimal(
                    str(
                        self.selling_price.value()
                    )
                ),

            "mrp":
                Decimal(
                    str(
                        self.mrp.value()
                    )
                ),

            "gst_percent":
                Decimal(
                    self.gst.currentText()
                ),

            "gst_type":
                self.gst_type.currentText(),

            "primary_unit_id":
                self.primary_unit.currentData(),

            "secondary_unit_id":
                self.secondary_unit.currentData(),

            "conversion_factor":
                self.conversion.value(),

            "opening_stock":
                self.opening_stock.value(),

            "minimum_stock":
                self.minimum_stock.value(),

            "maximum_stock":
                self.maximum_stock.value(),

            "reorder_level":
                self.reorder_level.value(),

            "image_path":
                self.image_path,

        }

        try:

            if self.product:

                self.product_service.update(
                    self.product.id,
                    **data,
                )

            else:

                self.product_service.create(
                    **data,
                )

            self.session.commit()

            self.accept()

        except Exception as exc:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Error",
                str(exc),
            )