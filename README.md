 # Microservices Shop

Микросервисный интернет-магазин на FastAPI + PostgreSQL.

## Стек
- Python 3.14
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Docker
- RabbitMQ
- Nginx

## Архитектура проекта
**Swagger**: `http://localhost:80/api/docs`
- **API Gateway** (/api_gateway): Единая точка входа для всех _клиентских запросов_ (помечены - ✅, требуется JWT-аутентификация - 🔐).
  - GET `/me` - Получение ID и почты пользователя ✅🔐


- **Auth Service** (/auth_service): Сервис аутентификации и авторизации. Отвечает за регистрацию, вход пользователей, выдачу и валидацию JWT-токенов. 
  - POST `/register` - Регистрация нового пользователя ✅
  - POST `/login` - Вход в систему ✅


- **Catalog Service** (/catalog_service): Сервис управления каталогом товаров. Предоставляет API для просмотра, поиска и управления товарами.
  - GET `/products` - Получить список всех товаров ✅
  - GET `/products/{product_id}` - Получить товар по ID ✅
  - POST `/products` - Создать новый товар
  - DELETE `/products/{iproduct_d}` - Удалить товар


- **Order Service** (`/order_service`): Сервис управления заказами. Обрабатывает создание заказов, проверку товаров и обновление статуса через RabbitMQ.
  - GET `/orders` - Получить список всех заказов 
  - GET `/orders/{order_id}` - Получить заказ по ID ✅🔐
  - POST `/orders` - Создать новый заказ ✅🔐



- **Payment Service** (`/payment_service`): Сервис обработки платежей. Выполняет имитацию оплаты, обновляет статус платежа и отправляет события в RabbitMQ.
  - GET `/payments` - Получить список платежей
  - GET `/payments/{id}` - Получить платёж по ID
  - POST `/payments` - Создать платёж

## Запуск
```bash
git clone https://github.com/tgmrv/microservices-shop.git
cd microservices-shop

docker-compose up -d --build

# Остановить сервис
docker-compose down

# Остановить сервис и удалить все данные
docker-compose down -v
```
