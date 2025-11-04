from fastapi import FastAPI, HTTPException, Query
from app.operations import add, subtract, multiply, divide

app = FastAPI(title="FastAPI Calculator")

# ----- POST Endpoints -----
@app.post("/add")
def add_numbers(payload: dict):
    try:
        x = payload["x"]
        y = payload["y"]
        return {"result": add(x, y)}
    except KeyError:
        raise HTTPException(status_code=400, detail="x and y are required")

@app.post("/subtract")
def subtract_numbers(payload: dict):
    try:
        x = payload["x"]
        y = payload["y"]
        return {"result": subtract(x, y)}
    except KeyError:
        raise HTTPException(status_code=400, detail="x and y are required")

@app.post("/multiply")
def multiply_numbers(payload: dict):
    try:
        x = payload["x"]
        y = payload["y"]
        return {"result": multiply(x, y)}
    except KeyError:
        raise HTTPException(status_code=400, detail="x and y are required")

@app.post("/divide")
def divide_numbers(payload: dict):
    try:
        x = payload["x"]
        y = payload["y"]
        return {"result": divide(x, y)}
    except KeyError:
        raise HTTPException(status_code=400, detail="x and y are required")
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")

# ----- Optional GET Endpoints for Browser Testing -----
@app.get("/add")
def add_numbers_get(x: float = Query(...), y: float = Query(...)):
    return {"result": add(x, y)}

@app.get("/subtract")
def subtract_numbers_get(x: float = Query(...), y: float = Query(...)):
    return {"result": subtract(x, y)}

@app.get("/multiply")
def multiply_numbers_get(x: float = Query(...), y: float = Query(...)):
    return {"result": multiply(x, y)}

@app.get("/divide")
def divide_numbers_get(x: float = Query(...), y: float = Query(...)):
    try:
        return {"result": divide(x, y)}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
