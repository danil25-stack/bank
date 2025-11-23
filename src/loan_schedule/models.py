from sqlalchemy import Column, Integer, Date, DECIMAL, Boolean, ForeignKey, String
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from src.database import Base


class LoanRepaymentScheduleItem(Base):
    __tablename__ = 'loan_repayment_schedule_item'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan.id"), nullable=False)
    installment_number = Column(String)
    due_date = Column(Date)
    principal_due = Column(String)
    interest_due = Column(String)
    total_due = Column(String)
    paid = Column(Boolean, default=False)
    paid_date = Column(Date, nullable=True)

    loan = relationship("Loan", back_populates="repayment_schedules")

    def encrypt_fields(self):
        self.principal_due = encrypt_data(str(self.principal_due))
        self.interest_due = encrypt_data(str(self.interest_due))
        self.total_due = encrypt_data(str(self.total_due))
        self. installment_number = encrypt_data(str(self.installment_number))

    def decrypt_fields(self):
        self.principal_due = float(decrypt_data(self.principal_due))
        self.interest_due = float(decrypt_data(self.interest_due))
        self.total_due = float(decrypt_data(self.total_due))
        self. installment_number = int(decrypt_data(self.installment_number))
