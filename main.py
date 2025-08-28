# main.py
"""
FastAPI Revision Playground 🚀
Author: Your Name
This file covers:
- Basic routes
- Path & query parameters
- Error handling
- Async routes
- Password hashing
- JSON request/response
- CRUD operations (with Pydantic models)
- Dependency Injection
- Middleware & custom headers
- Form & Body parsing
- Response models
"""

from fastapi import FastAPI, HTTPException, Depends, Form, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext
import asyncio

# Create FastAPI app instance
app = FastAPI(title="FastAPI Revision API", version="2.0")

# ------------------------
# 1. Basic GET endpoint
# ------------------------
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

# ------------------------
# 2. Path Parameter
# ------------------------
@app.get("/speed/{speed}")
def display(speed: int):
    return {"speed": speed, "info": f"Your speed is {speed}"}

# ------------------------
# 3. Error Handling Example
# ------------------------
@app.get("/test/{speed}")
def verify(speed: int):
    if speed != 100:
        raise HTTPException(status_code=404, detail="Speed does not match")
    return {"status": "success", "speed": speed}

# ------------------------
# 4. Query Parameters
# ------------------------
@app.get("/search")
def check(item: int, limit: int = 10):
    return {"item": item, "limit": limit}

# ------------------------
# 5. Async Endpoint (Simulated delay)
# ------------------------
@app.get("/ui")
async def get():
    await asyncio.sleep(2)  # Simulating delay
    return {"message": "Hello Global"}

# ------------------------
# 6. Password Hashing
# ------------------------
@app.get("/pass/{passwd}")
def passwd(passwd: str):
    pwd_cont = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_cont.hash(passwd)
    return {
        "original_password": passwd,
        "hashed_password": hashed_pwd
    }

# ------------------------
# 7. JSON with Pydantic Model
# ------------------------
class User(BaseModel):
    id: int
    name: str
    email: str

@app.post("/user/")
def create_user(user: User):
    return {"msg": "User created", "data": user}

# ------------------------
# 8. CRUD (In-Memory DB)
# ------------------------
db = {}

@app.post("/items/")
def create_item(item_id: int, name: str):
    if item_id in db:
        raise HTTPException(status_code=400, detail="Item already exists")
    db[item_id] = name
    return {"msg": "Item added", "db": db}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": db[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = name
    return {"msg": "Item updated", "db": db}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"msg": "Item deleted", "db": db}

# ------------------------
# 9. Dependency Injection Example
# ------------------------
def verify_token(token: str = Header(...)):
    if token != "secret123":
        raise HTTPException(status_code=403, detail="Invalid token")
    return True

@app.get("/secure-data", dependencies=[Depends(verify_token)])
def secure():
    return {"msg": "This is protected data"}

# ------------------------
# 10. Middleware Example
# ------------------------
@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "FastAPI-Revision"
    return response

# ------------------------
# 11. Form & Body Parsing
# ------------------------
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        return {"msg": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ------------------------
# 12. Response Model
# ------------------------
class Item(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items/", response_model=Item)
def create_item_with_model(item: Item):
    return item
