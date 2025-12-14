from fastapi import FastAPI
import uvicorn

from src.consent.routes import router as consent_router
from src.account.router import router as account_router
from src.loan.router import router as loan_router
from src.psu.router import router as psu_router
from src.balance.router import router as balance_router
from src.transaction.router import router as transaction_router
from src.loan_schedule.router import router as loan_schedule_router
from src.auth.router import router as auth_router


app = FastAPI()

# =========================
# ROUTERS
# =========================

app.include_router(consent_router)
app.include_router(account_router)
app.include_router(loan_router)
app.include_router(psu_router)
app.include_router(balance_router)
app.include_router(transaction_router)
app.include_router(loan_schedule_router)
app.include_router(auth_router)


# =========================
# HEALTHCHECK
# =========================

@app.get("/")
def index():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
