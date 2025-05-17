import os
import sqlite3
import bcrypt
import jwt
import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import htmx
import uvicorn
from fastapi.middleware import Middleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import logging

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# Database connection
def get_db():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")

# User models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

# Create database tables
def create_tables():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT,
                full_name TEXT,
                disabled BOOLEAN,
                hashed_password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plan TEXT,
                price REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    except Exception as e:
        logger.error(f"Database table creation error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database table creation error")
    finally:
        conn.close()

create_tables()

# Password hashing
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Get user by username
def get_user(db: sqlite3.Connection, username: str) -> Optional[UserInDB]:
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        if user_row:
            return UserInDB(**dict(user_row))
        return None
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user")

# Create user
def create_user(db: sqlite3.Connection, user: UserCreate) -> UserInDB:
    try:
        hashed_password = get_password_hash(user.password)
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, full_name, disabled, hashed_password)
            VALUES (?, ?, ?, ?, ?)
        """, (user.username, user.email, user.full_name, False, hashed_password))
        db.commit()
        return get_user(db, user.username)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")

# Generate token
def generate_token(data: Dict[str, Any], expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# Get refresh token
def get_refresh_token(data: Dict[str, Any]) -> str:
    return generate_token(data, datetime.timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS))

# Decode token
def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Token refresh
def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    payload = decode_token(refresh_token)
    if not payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return {
        "access_token": generate_token({"sub": payload["sub"]}),
        "token_type": "bearer"
    }

# Dependency for database
def get_db_dependency():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Dependency for current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except HTTPException:
        raise credentials_exception
    user = get_user(db=get_db(), username=username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        db = get_db()
        user = get_user(db, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token_expires = datetime.timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = generate_token({"sub": user.username}, access_token_expires)
        refresh_token = get_refresh_token({"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login error")

@app.post("/token/refresh", response_model=Token)
@limiter.limit("5/minute")
async def refresh_token(token: TokenRefreshRequest):
    try:
        payload = decode_token(token.refresh_token)
        if not payload.get("sub"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return {"access_token": generate_token({"sub": payload["sub"]}), "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Refresh token error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Refresh token error")

@app.post("/users", response_model=UserInDB)
async def create_new_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db_dependency)):
    return create_user(db, user)

@app.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@app.get("/users")
async def read_users(db: sqlite3.Connection = Depends(get_db_dependency)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        users = [UserInDB(**dict(row)) for row in cursor.fetchall()]
        return users
    except Exception as e:
        logger.error(f"Error reading users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error reading users")

# Other routes
@app.get("/")
async def read_root():
    return {"message": "Hello World"}