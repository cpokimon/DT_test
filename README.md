# DT_test

##### Postman collection: [GitHub](http://github.com)

##### Quick start:
  1. ##### git clone https://github.com/cpokimon/DT_test.git
  2. docker-compose up --build        ---> ufter building process open a new terminal
  3. docker ps                        ---> now we need to find the container named "dt_test_app" and copy id (f.e 9aaced99f547)
  4. docker exec -it <place here copied id> sh
  5. python manage.py migrate
  6. open browser and open address 'localhost'
