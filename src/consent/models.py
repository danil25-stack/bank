from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, JSON
from src.utils.crypto import encrypt_data, decrypt_data
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
import json


class Consent(Base):
    __tablename__ = 'consent'

    id = Column(Integer, primary_key=True, index=True)
    psu_id = Column(Integer, ForeignKey("psu.id"), nullable=False)
    access = Column(JSON)
    recurring_indicator = Column(Boolean)
    valid_until = Column(Date)
    frequency_per_day = Column(String)
    combined_service_indicator = Column(Boolean)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    psu = relationship("Psu", back_populates="consents")

    def encrypt_fields(self):
        self.access = encrypt_data(json.dumps(self.access))
        self.status = encrypt_data(self.status)
        self.frequency_per_day = encrypt_data(self.frequency_per_day)

    def decrypt_fields(self):
        self.access = json.loads(decrypt_data(self.access))
        self.status = decrypt_data(self.status)
        self.frequency_per_day = decrypt_data(self.frequency_per_day)
