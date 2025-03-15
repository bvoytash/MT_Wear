import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # to delete
from fastapi.middleware.cors import CORSMiddleware
from routes import users, auth
from database import Base, engine

# Don't forget to import the models
from models.users import User


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # to delete
Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(auth.router)

origins = [
    "http://frontendurl.uk",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(content={"detail": "The server is working"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, workers=4, reload=True
    )  # remove reload when finished with testing
