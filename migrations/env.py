import os
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# --- MODELS ---
from src.database import Base, sync_engine   # <-- IMPORTANT FIX
from src.psu.models import Psu
from src.account.models import Account
from src.consent.models import Consent
from src.loan.models import Loan
from src.balance.models import Balance
from src.transaction.models import Transaction
from src.loan_schedule.models import LoanRepaymentScheduleItem

config = context.config

# Fix sqlalchemy.url in Docker
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option(
        "sqlalchemy.url",
        os.getenv("DATABASE_URL", "postgresql://admin:admin@db:5432/bank")
    )

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialet_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with sync_engine.connect() as connection:   # <-- FIXED
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
