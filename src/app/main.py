from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_db
from app.schemas import UserCreate, UserResponse


app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}

@app.get("/users", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(User.__table__.select())
    return result.scalars().all()

@app.get("/user/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@app.post("/user", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user