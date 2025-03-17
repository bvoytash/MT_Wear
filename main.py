import os
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from routes import users, products, category
from fastapi.staticfiles import StaticFiles  # to delete
from fastapi.middleware.cors import CORSMiddleware
from routes import users, auth
from database import Base, engine

# Don't forget to import the models
from models.users import User

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # to delete
Base.metadata.create_all(bind=engine)
# app.include_router(users.router)
app.include_router(products.router)
app.include_router(category.router)
app.include_router(users.router)
app.include_router(auth.router)

origins = [
    "http://127.0.0.1:5500",  # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'"
    )

    return response


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(
        content={"detail": "The server is working"}, status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, workers=4, reload=True
    )  # remove reload when finished with testing
