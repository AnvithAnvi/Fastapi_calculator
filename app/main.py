from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, SessionLocal

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator with PostgreSQL")

# --------------------------------------------------------------------
# Utility: create a default user on startup (fixes FK violation)
# --------------------------------------------------------------------
def ensure_default_user():
    """Ensure there is at least one default user in the database."""
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        default_user = models.User(username="default", email="default@example.com")
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        print("✅ Default user created:", default_user.username)
    db.close()


@app.on_event("startup")
def startup_event():
    """Run on app startup — ensure DB is initialized."""
    ensure_default_user()
    print("🚀 FastAPI app started and default user ensured.")


# --------------------------------------------------------------------
# Dependency
# --------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Calculator!"}


@app.post("/add")
def add_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload.get("x")
    y = payload.get("y")
    result = x + y

    # Ensure the user exists (FK safety)
    ensure_default_user()

    calc = models.Calculation(
        operation="add",
        operand_a=x,
        operand_b=y,
        result=result,
        user_id=1,  # always link to default user
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}


@app.post("/subtract")
def subtract_numbers(payload: dict, db: Session = Depends(get_db)):
    x = payload.get("x")
    y = payload.get("y")
    result = x - y

    ensure_default_user()

    calc = models.Calculation(
        operation="subtract",
        operand_a=x,
        operand_b=y,
        result=result,
        user_id=1,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return {"result": result, "calculation_id": calc.id}
