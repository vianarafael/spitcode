# SQLite Usage Patterns for FastAPI SaaS Apps

This document outlines effective patterns and best practices for using SQLite in small-scale SaaS applications, particularly with Python and FastAPI.

---

## When to Use SQLite

* **Rapid prototyping** and MVPs
* **Single-user** or low-concurrency web apps
* Local desktop or mobile applications
* **Read-heavy** workloads with minimal concurrent writes

> ❗ Avoid using SQLite for high-concurrency, write-heavy SaaS applications. Use PostgreSQL or MySQL in production.

---

## Project Layout

```bash
saas-app/
├── main.py
├── database.py
├── models.py
├── crud.py
├── routers/
│   └── users.py
├── schemas.py
└── requirements.txt
```

---

## Connecting to SQLite

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## Dependency Injection for DB Session

```python
# main.py
from fastapi import Depends, FastAPI
from .database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Models

```python
# models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

---

## CRUD Utilities

```python
# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

---

## SQLite-Specific Tips

* Use `check_same_thread=False` if you're using SQLite across threads (common in FastAPI)
* Avoid storing large blobs or files—store paths instead
* Use `PRAGMA` for performance tuning:

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
```

* Backup with `sqlite3` CLI:

```bash
sqlite3 app.db ".backup backup.db"
```

---

## Security Tips

* Never expose `.db` files over the internet
* Validate all input before inserting into SQLite
* Use parameterized queries or SQLAlchemy ORM to avoid SQL injection

---

## Testing with SQLite

Use an in-memory DB for tests:

```python
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
```

---

## Migration Strategy

* Use [Alembic](https://alembic.sqlalchemy.org/) with care: SQLite has limited ALTER TABLE support
* Alternatively: dump data, recreate schema, and reinsert

---

## Resources

* [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
* [https://www.sqlite.org/lang.html](https://www.sqlite.org/lang.html)
* [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/)
