from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    yield

    # Application shutdown
    await engine.dispose()


app = FastAPI(
    title="FastAPI Neon Database",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "message": "FastAPI is running"
    }


@app.get("/health")
async def health_check():
    async with engine.connect() as connection:
        result = await connection.execute(
            text("SELECT 1")
        )

        return {
            "database": "connected",
            "result": result.scalar_one(),
        }