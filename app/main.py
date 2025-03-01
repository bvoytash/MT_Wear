from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import text

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Store API is running!"}


@app.get("/ping_db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))  # Test query
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": str(e)}