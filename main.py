from os import getenv
from uvicorn import run
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import users, auth, products, category, shopping_bag, orders
from database import Base, engine

# Don't forget to import the models
from models.users import User
from models.product import Product
from models.category import Category

FRONTEND_URL = getenv("FRONTEND_URL")
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(category.router)
app.include_router(shopping_bag.router)
app.include_router(orders.router)

app.include_router(users.router)
app.include_router(auth.router)

origins = [
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [err["msg"] for err in exc.errors()]
    error_response = {"detail": ", ".join(error_messages)}
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response
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
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js 'sha256-QOOQu4W1oxGqd2nbXbxiA1Di6OHQOLQD+o+G9oWL8YY='; "
        "style-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css; "
        "img-src 'self' https://fastapi.tiangolo.com data:; http://www.w3.org/2000/svg;"
        "frame-ancestors 'none'"
    )

    return response


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(
        content={"detail": "The server is working"}, status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    run(
        "main:app", host="0.0.0.0", port=8000, workers=4, reload=True
    )  # remove reload when finished with testing
