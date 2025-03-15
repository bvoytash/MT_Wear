For manual testing:
http://localhost:8000/static/manual_test.html

To setup the database you need an .env file with this variables:
SQLALCHEMY_DATABASE_URL
SECRET_KEY
ALGORITHM

Example:
SQLALCHEMY_DATABASE_URL=sqlite:///local.db
SECRET_KEY="e104cc05b88ec7ce74aae28e32"
ALGORITHM="HS256"
