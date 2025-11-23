from sqlalchemy import Column, Integer, String
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class Psu(Base):
    __tablename__ = 'psu'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, primary_key=False, index=False, unique=False)
    email = Column(String, primary_key=False, index=True, unique=True)

    accounts = relationship("Account", back_populates="psu")
    consents = relationship("Consent", back_populates="psu")
    loans = relationship("Loan", back_populates="psu")

    def encrypt_fields(self):
        self.name = encrypt_data(str(self.name))
        self.email = encrypt_data(str(self.email))

    def decrypt_fields(self):
        self.name = decrypt_data(str(self.name))
        self.email = decrypt_data(str(self.email))
