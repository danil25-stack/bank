from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    transaction_type = Column(String)  # debit | credit
    booking_date = Column(Date)
    value_date = Column(Date)
    amount = Column(String)
    currency = Column(String)
    creditor_name = Column(String, nullable=True)
    debtor_name = Column(String, nullable=True)
    remittance_information = Column(String, nullable=True)

    account = relationship("Account", back_populates="transactions")

    def encrypt_fields(self):
        self.transaction_type = encrypt_data(self.transaction_type)
        self.amount = encrypt_data(str(self.amount))
        self.currency = encrypt_data(self.currency)
        self.creditor_name = encrypt_data(self.creditor_name)
        self.debtor_name = encrypt_data(self.debtor_name)
        self.remittance_information = encrypt_data(self.remittance_information)

    def decrypt_fields(self):
        self.transaction_type = decrypt_data(self.transaction_type)
        self.amount = float(decrypt_data(self.amount))
        self.currency = decrypt_data(self.currency)
        self.creditor_name = decrypt_data(self.creditor_name)
        self.debtor_name = decrypt_data(self.debtor_name)
        self.remittance_information = decrypt_data(self.remittance_information)
