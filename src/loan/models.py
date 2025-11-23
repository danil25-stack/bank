from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, Date
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class Loan(Base):
    __tablename__ = 'loan'

    id = Column(Integer, primary_key=True, unique=True)
    psu_id = Column(Integer, ForeignKey("psu.id"), nullable=False)
    repayment_account_id = Column(
        Integer, ForeignKey("account.id"), nullable=False)
    principal_amount = Column(String)
    currency = Column(String)
    interest_rate = Column(String)
    term_months = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    psu = relationship("Psu", back_populates="loans")
    account = relationship("Account", back_populates="loans")
    repayment_schedules = relationship(
        "LoanRepaymentScheduleItem",
        back_populates="loan",
        cascade="all, delete-orphan"
    )

    def encrypt_fields(self):
        self.principal_amount = encrypt_data(str(self.principal_amount))
        self.currency = encrypt_data(self.currency)
        self.interest_rate = encrypt_data(str(self.interest_rate))
        self.term_months = encrypt_data(str(self.term_months))
        self.status = encrypt_data(self.status)

    def decrypt_fields(self):
        self.principal_amount = float(decrypt_data(self.principal_amount))
        self.interest_rate = float(decrypt_data(self.interest_rate))
        self.term_months = int(decrypt_data(self.term_months))
        self.currency = decrypt_data(self.currency)
        self.status = decrypt_data(self.status)
