# src/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine  # <-- ДЛЯ ALEMIBC ONLY!

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:admin@db:5432/bank"
)

# ⚠️ PS: ДЛЯ ALEMIBC нужен sync URL
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")  # psycopg2

# Async Engine (FastAPI)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)

# Sync Engine (Alembic)
sync_engine = create_engine(SYNC_DATABASE_URL)

Base = declarative_base()

from src.psu.models import Psu
from src.account.models import Account
from src.consent.models import Consent
from src.loan.models import Loan
from src.balance.models import Balance
from src.transaction.models import Transaction
from src.loan_schedule.models import LoanRepaymentScheduleItem
from src.auth.models import User

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
