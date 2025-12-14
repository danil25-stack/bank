from enum import Enum


class SourceType(str, Enum):
    ATM = "ATM"
    BANK_TRANSFER = "BANK_TRANSFER"
    POS = "POS"
    SALARY = "SALARY"
    COMMERCE_PAYMENTS = "COMMERCE_PAYMENTS"
