from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_db
from app.schemas import UserCreate, UserResponse


app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}


# Get All Users
@app.get("/users", response_model=list[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users


# Get User By ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# Create User
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        db_user = User(
            name=user.name,
            email=user.email
        )

        db.add(db_user)

        await db.commit()
        await db.refresh(db_user)

        return db_user

    except Exception:
        await db.rollback()
        raise
    
    
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return {
        "message": "User deleted successfully"
    }    