import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from routes import users
from database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(content={"detail": "The server is working"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
