Here's a layered architecture approach combining repository pattern, interface segregation, and code generation:

## Business Layer Implementation
**Domain models** (pure Python classes):
```python
# Pure business objects with type hints
class User:
    def __init__(self, id: int, username: str, email: str):
        self.id = id  # Domain ID (not tied to DB PK)
        self.username = username
        self.email = email

class UserCreate:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
```

## Abstraction Layer
**Generic repository interface** (ISP-compliant):
```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')
K = TypeVar('K')

class Repository(ABC):
    @abstractmethod
    def get(self, id: K) -> T:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> K:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        pass
```

## SQL Implementation Layer
**SQLAlchemy models** (generated from domain annotations):
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Auto-generated using type annotations + codegen tool
class SQLUser(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(120))
```

**Adapter implementation** (converts domain ↔ SQL):
```python
class SQLUserRepository(Repository):
    def __init__(self, session):
        self.session = session
        
    def get(self, user_id: int) -> User:
        db_user = self.session.query(SQLUser).get(user_id)
        return User(db_user.id, db_user.username, db_user.email)
    
    def add(self, user: User) -> int:
        db_user = SQLUser(**user.__dict__)
        self.session.add(db_user)
        self.session.flush()
        return db_user.id
```

## DRY Code Generation
**Annotation-based schema definition** (shared across layers):
```python
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import mapped_column

# Shared type annotations
UUIDStr = Annotated[str, mapped_column(String(36))]
Email = Annotated[str, mapped_column(String(120))]

# Business model with shared annotations
class Product(BaseModel):
    id: UUIDStr
    name: str
    price: float
    contact_email: Email
```

**Code generation workflow**:
1. Annotate domain models with SQL-specific metadata[8]
2. Use `sqlacodegen`[7] or custom templates to generate:
   - SQLAlchemy models
   - Pydantic validation schemas
   - Repository adapter classes

## Key Architecture Benefits
**Separation of concerns**:
| Layer              | Responsibility              | SQL Awareness |
|--------------------|-----------------------------|---------------|
| Business Logic     | Domain models + operations  | None          |
| Repository         | CRUD interface definition   | Abstract      |
| SQL Implementation | ORM mapping + transactions | Full          |

**Maintainability features**:
- **Interface-first design**: Business logic only interacts with `Repository` abstract base class[3][5]
- **Bi-directional adapters**: Convert between domain objects and persistence models[1][4]
- **Schema registry**: Central type annotations enforce consistency[8]
- **Testability**: Swap SQL implementation with in-memory repository for unit tests[1]

This approach enables database engine swaps (SQL → NoSQL) without modifying business logic, while maintaining type safety and reducing boilerplate through code generation.
