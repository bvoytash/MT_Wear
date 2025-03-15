For manual testing:
http://localhost:8000/static/manual_test.html

To setup the database you need an .env file with this variable:
SQLALCHEMY_DATABASE_URL

Example:
SQLALCHEMY_DATABASE_URL=sqlite:///local.db






curl -X DELETE \
  http://localhost:8000/users/delete-page \
  -H 'Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhQGFidi5iZyIsImV4cCI6MTc0MjAwMTI3M30.Ag3vQJnvfui50nLHOHUEKf6EmZZ43jFSVTPFWVVPbCQ'


curl -X DELETE \
  http://localhost:8000/users/delete \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhQGFidi5iZyIsImV4cCI6MTc0MjAwMTI3M30.Ag3vQJnvfui50nLHOHUEKf6EmZZ43jFSVTPFWVVPbCQ'



curl -X POST \
  http://localhost:8000/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=a@abv.bg&password=22'



curl -X POST \
  http://localhost:8000/auth/logout \
  -H 'Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhQGFidi5iZyIsImV4cCI6MTc0MjAwMTI3M30.Ag3vQJnvfui50nLHOHUEKf6EmZZ43jFSVTPFWVVPbCQ'


decide approach