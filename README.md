#### For manual testing use manual_test.html
##### To simulate the fronend serve the html file with Live Server extention (vscode)

#### To setup the database you need an .env file with this variables:
- SQLALCHEMY_DATABASE_URL
- SECRET_KEY
- ALGORITHM
- MASTER_PASSWORD
- COOKIE_MAX_AGE
- COOKIE_DELTA
- CSRF_TOKEN_SIZE
- FRONTEND_URL

Example:
```
SQLALCHEMY_DATABASE_URL=sqlite:///local.db
SECRET_KEY="e104cc05b88ec7ce74aae28e32"
ALGORITHM="HS256"
MASTER_PASSWORD="d104cc05ba8ec7ce74aae28e31"
COOKIE_MAX_AGE=1800
COOKIE_DELTA=30
CSRF_TOKEN_SIZE=64
FRONTEND_URL="http://127.0.0.1:5500"
```
