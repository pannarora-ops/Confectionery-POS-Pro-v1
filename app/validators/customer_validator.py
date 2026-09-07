"""
Customer validator.
"""

import re


class CustomerValidator:

    @staticmethod
    def validate_name(name: str):

        if not name.strip():
            raise ValueError(
                "Customer name is required."
            )

    @staticmethod
    def validate_phone(phone: str | None):

        if phone is None:
            return

        if not re.fullmatch(r"\d{10}", phone):
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )