When implementing CRUD operations with SQLAlchemy and Pydantic, here's a standard approach:

## Database Model Implementation
**Primary key declaration** should use explicit column definitions:
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Standard primary key [5]
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
```

For **Pydantic models**, enable ORM compatibility:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int  # Mirror primary key from SQLAlchemy [2]
    username: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode [1]
```

## CRUD Operations
**GET operations** should use:
```python
# Get by primary key (most efficient)
user = session.get(User, user_id)  # Returns None if not found [6][8]

# Filter with conditions
users = session.execute(select(User).where(User.username == "john")).scalars().all()
```

**UPDATE operations** typically use:
```python
# ORM style
user = session.get(User, user_id)
user.email = "new@email.com"
session.commit()

# Core UPDATE statement (better for bulk)
stmt = update(User).where(User.id == user_id).values(email="new@email.com")
session.execute(stmt)
session.commit()  # [7]
```

## Key Considerations
1. **Primary Key Best Practices**
   - Use `autoincrement=True` for surrogate keys[5]
   - Prefer integer keys over natural keys for joins
   - For composite keys, use `primary_key=True` on multiple columns

2. **Model Relationships**
   - Use SQLAlchemy relationships for joins:
   ```python
   class Post(Base):
       __tablename__ = 'posts'
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey('users.id'))
       user = relationship("User", back_populates="posts")
   ```

3. **Validation Layer**
   - Separate Pydantic models for create/update/response schemas
   - Use `EmailStr` and other Pydantic validators for input sanitation[2]

For reduced duplication, consider:
- **SQLModel** (combines SQLAlchemy+Pydantic)[1][9]
- **pydantic-sqlalchemy** for auto-generated models:
  ```python
  from pydantic_sqlalchemy import sqlalchemy_to_pydantic
  
  PydanticUser = sqlalchemy_to_pydantic(User)  # Auto-generates model [3]
  ```

This pattern ensures type safety while maintaining database efficiency, with Pydantic handling validation/Serialization and SQLAlchemy managing database interactions.
