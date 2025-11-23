from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    balance_type = Column(String)  # available / booked
    amount = Column(String)
    currency = Column(String)
    reference_date = Column(Date)

    account = relationship("Account", back_populates="balances")

    def encrypt_fields(self):
        self.balance_type = encrypt_data(self.balance_type)
        self.amount = encrypt_data(str(self.amount))
        self.currency = encrypt_data(self.currency)

    def decrypt_fields(self):
        self.balance_type = decrypt_data(self.balance_type)
        self.amount = float(decrypt_data(self.amount))
        self.currency = decrypt_data(self.currency)
