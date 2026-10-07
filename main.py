from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

Base.metadata.create_all(bind=engine)
app = FastAPI(title="가계부 API")

@app.post("/accounts", response_model=schemas.AccountRead, status_code=201)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    account = models.Account(name=payload.name, balance=payload.balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@app.get("/accounts", response_model=list[schemas.AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return db.execute(select(models.Account).order_by(models.Account.id)).scalars().all()

@app.get("/accounts/{account_id}", response_model=schemas.AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(models.Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="계좌를 찾을 수 없습니다")
    return account

@app.post("/transactions", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    if db.get(models.Account, payload.account_id) is None:
        raise HTTPException(status_code=404, detail="해당 계좌가 없습니다")
    tx = models.Transaction(account_id=payload.account_id, category_id=payload.category_id,
                            amount=payload.amount, memo=payload.memo)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@app.get("/accounts/{account_id}/detail", response_model=schemas.AccountReadWithTx)
def account_detail(account_id: int, db: Session = Depends(get_db)):
    account = db.get(models.Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="계좌 없음")
    return account

@app.get("/stats/by-category")
def by_category(db: Session = Depends(get_db)):
    stmt = (
        select(models.Category.name, func.sum(models.Transaction.amount), func.count())
        .join(models.Category, models.Transaction.category_id == models.Category.id, isouter=True)
        .where(models.Transaction.amount < 0)
        .group_by(models.Category.name)
    )
    return [{"category": n, "total": t, "count": c} for n, t, c in db.execute(stmt).all()]
