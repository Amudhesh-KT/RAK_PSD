from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext

client = MongoClient('mongodb+srv://damudheshkt:Amudhesh_rasa@cluster0.upd64s4.mongodb.net/')
db = client['RAK_PSD']
collection = db['Users']

app = FastAPI()
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    location: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: UserRegister):
    # Check if user already exists
    if collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    # Store user in database
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "location": user.location
    }
    collection.insert_one(user_data)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    print(user)
    # Find the user in the database
    db_user = collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # Verify the password
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    username = db_user.get("username")
    email = db_user.get("email")
    location = db_user.get("location")
    response = {
        "username": username,
        "email": email,
        "location": location
    }
    return {"message": "Login successful", "user": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)