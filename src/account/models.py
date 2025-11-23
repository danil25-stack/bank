from sqlalchemy import Column, Integer, String, ForeignKey
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, primary_key=False, index=False)
    iban = Column(String, primary_key=False, index=False)
    currency = Column(String, primary_key=False, index=False)
    product = Column(String, primary_key=False, index=False)
    cash_account_type = Column(String, primary_key=False, index=False)
    name = Column(String, primary_key=False, index=False)
    psu_id = Column(Integer, ForeignKey("psu.id"), nullable=False)

    psu = relationship("Psu", back_populates="accounts")
    loans = relationship("Loan", back_populates="account")
    balances = relationship("Balance", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")

    def encrypt_fields(self):
        self.iban = encrypt_data(self.iban)
        self.currency = encrypt_data(self.currency)
        self.product = encrypt_data(self.product)
        self.cash_account_type = encrypt_data(self.cash_account_type)
        self.name = encrypt_data(self.name)

    def decrypt_fields(self):
        self.iban = decrypt_data(self.iban)
        self.currency = decrypt_data(self.currency)
        self.product = decrypt_data(self.product)
        self.cash_account_type = decrypt_data(self.cash_account_type)
        self.name = decrypt_data(self.name)
