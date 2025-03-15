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




#### delete
fetch('http://localhost:8000/users/delete', {
  method: 'DELETE',
  credentials: 'include'
})
.then(response => console.log(response))
.catch(error => console.error('Error:', error));

#### login
fetch('http://localhost:8000/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: 'email=a@abv.bg&password=22'
})
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

#### logout
fetch('http://localhost:8000/logout', {
  method: 'POST',
})
.then(response => console.log(response))
.catch(error => console.error('Error:', error));

#### create
fetch('http://localhost:8000/users/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: 'email=a@abv.bg&password=22'
})
.then(data => console.log(data))
.catch(error => console.error('Error:', error));