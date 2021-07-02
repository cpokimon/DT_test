# DT_test

##### [Postman collection](https://www.getpostman.com/collections/f363478ae427eae10f16)

##### Quick start:
  1. git clone https://github.com/cpokimon/DT_test.git
  2. docker-compose up --build        ---> ufter building process open a new terminal
  4. docker-compose exec app sh
  5. python manage.py migrate
  6. python manage.py test (optional) ---> run tests
  7. python manage.py createsuperuser (add login, email, pass) 
  8. open browser, open address 'localhost/admin' and login
  9. create several records in tables "Posts" and "Comments"
  10. open browser and open address 'localhost'
