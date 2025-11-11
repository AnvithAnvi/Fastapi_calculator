from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add")
def add_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload["x"]
    y = payload["y"]
    result = x + y
    calc = models.Calculation(operation="add", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}


@app.post("/subtract")
def subtract_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload["x"]
    y = payload["y"]
    result = x - y
    calc = models.Calculation(operation="subtract", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}


@app.post("/multiply")
def multiply_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload["x"]
    y = payload["y"]
    result = x * y
    calc = models.Calculation(operation="multiply", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}


@app.post("/divide")
def divide_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload["x"]
    y = payload["y"]
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    result = x / y
    calc = models.Calculation(operation="divide", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}
