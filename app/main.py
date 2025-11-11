# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.operations import add, subtract, multiply, divide
from app.database import SessionLocal, engine
from app import models

# Initialize DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Calculator with PostgreSQL",
    description="A calculator API that logs all operations to a PostgreSQL database using Docker Compose and pgAdmin.",
    version="1.0.0",
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Calculator!"}


@app.post("/add")
def add_numbers(payload: dict, db: Session = Depends(get_db)):
    x, y = payload["x"], payload["y"]
    result = add(x, y)

    db_calc = models.Calculation(operation="add", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(db_calc)
    db.commit()
    return {"result": result}


@app.post("/subtract")
def subtract_numbers(payload: dict, db: Session = Depends(get_db)):
    x, y = payload["x"], payload["y"]
    result = subtract(x, y)

    db_calc = models.Calculation(operation="subtract", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(db_calc)
    db.commit()
    return {"result": result}


@app.post("/multiply")
def multiply_numbers(payload: dict, db: Session = Depends(get_db)):
    x, y = payload["x"], payload["y"]
    result = multiply(x, y)

    db_calc = models.Calculation(operation="multiply", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(db_calc)
    db.commit()
    return {"result": result}


@app.post("/divide")
def divide_numbers(payload: dict, db: Session = Depends(get_db)):
    x, y = payload["x"], payload["y"]

    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")

    result = divide(x, y)
    db_calc = models.Calculation(operation="divide", operand_a=x, operand_b=y, result=result, user_id=1)
    db.add(db_calc)
    db.commit()
    return {"result": result}


@app.get("/history")
def get_all_calculations(db: Session = Depends(get_db)):
    records = db.query(models.Calculation).all()
    return records
