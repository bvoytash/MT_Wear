#### For manual testing use /static/manual_test.html
##### To simulate the fronend serve the app with Live Server extention (vscode)

#### To setup the database you need an .env file with this variables:
- SQLALCHEMY_DATABASE_URL
- SECRET_KEY
- ALGORITHM
- MASTER_PASSWORD

Example:
```
SQLALCHEMY_DATABASE_URL=sqlite:///local.db
SECRET_KEY="e104cc05b88ec7ce74aae28e32"
ALGORITHM="HS256"
MASTER_PASSWORD="d104cc05ba8ec7ce74aae28e31"
```
