# Microservices Shop

Backend интернет-магазина на FastAPI. Проект демонстрирует
аутентификацию пользователей, создание заказов, взаимодействие сервисов
по HTTP и обработку событий через RabbitMQ.

Оплата имитируется автоматически: Payment Service ожидает три секунды,
помечает платёж завершённым и публикует событие. Реальные списания
не выполняются.

## Стек
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Docker
- RabbitMQ
- Nginx
- pytest

## Архитектура проекта
Клиент отправляет запросы в **API Gateway** через **Nginx** на порту **80**.

**Gateway** предоставляет внешний API и проверяет JWT для защищённых маршрутов.

| Сервис | Ответственность |
|---|---|
| API Gateway | Маршрутизация запросов, проверка JWT и владельца заказа |
| Auth Service | Регистрация, проверка паролей и выдача JWT |
| Catalog Service | Хранение и получение товаров |
| Order Service | Расчёт стоимости, сохранение заказов и обработка событий оплаты |
| Payment Service | Создание платежей, имитация оплаты и публикация событий |

Order Service обращается к Catalog Service и Payment Service по HTTP.
События об успешной оплате передаются из Payment Service в Order Service
через RabbitMQ.

## Внешний API

Все пути указаны относительно API Gateway.

| Метод | Путь | Назначение | Требуется JWT |
|---|---|---|---|
| POST | `/api/auth/register` | Регистрация | Нет |
| POST | `/api/auth/login` | Вход | Нет |
| GET | `/api/auth/me` | Текущий пользователь | Да |
| GET | `/api/products` | Список товаров | Нет |
| GET | `/api/products/{product_id}` | Получение товара | Нет |
| POST | `/api/orders` | Создание заказа и запуск имитации оплаты | Да |
| GET | `/api/orders/{order_id}` | Получение своего заказа | Да |

Токен передаётся в заголовке:

```http
Authorization: Bearer <access_token>
```

При создании заказа Gateway заменяет переданный `user_id`
идентификатором пользователя из JWT.

Создание и удаление товаров, а также методы работы с платежами
реализованы во внутренних сервисах и не представлены маршрутами Gateway.

## Запуск

Требуются Docker и Docker Compose.

```bash
git clone https://github.com/tgmrv/microservices-shop.git
cd microservices-shop
docker-compose up -d --build
```

**Swagger UI**: `http://localhost:80/api/docs`

Остановка:

```bash
docker-compose down
```

## Тестирование

В проекте есть тесты API, бизнес-логики и обработки события оплаты.

Для тестирования работы с БД используется SQLite в памяти.
Внешние HTTP-вызовы и публикация событий подменяются моками.