# Todo List API

Простое и эффективное API для управления задачами с аутентификацией пользователей.

## Описание

RESTful API для todo-листа с поддержкой:
- Регистрации и аутентификации пользователей
- Создания, чтения, обновления и удаления задач
- JWT-аутентификации
- Работы с PostgreSQL или in-memory базой данных

## Установка

### Предварительные требования
- Python 3.13+
- Poetry (для управления зависимостями)
- Docker и Docker Compose (для запуска с PostgreSQL)

### Установка зависимостей
```bash
poetry install
```

## Запуск

Выбор базы данных зависит от переменной окружения `ENV`:
- `ENV=local` - используется хранилище в памяти
- `ENV=prod` - используется PostgreSQL

### Локальный запуск
```bash
# Создайте .env файл на основе примера
cp .env.example .env

# Запустите приложение
poetry run python -m todo_list_api.main
```

### Запуск с PostgreSQL через Docker
```bash
# Создайте .env файл и настройте параметры PostgreSQL
cp .env.example .env

# Установите ENV=prod для использования PostgreSQL
echo "ENV=prod" >> .env

# Запустите контейнеры
docker-compose up --build
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Использование API

### Аутентификация

#### Регистрация пользователя
```bash
POST /api/users/register
Content-Type: application/json

{
  "username": "user1",
  "email": "user@example.com",
  "password": "password123"
}
```

#### Авторизация пользователя
```bash
POST /api/users/login
Content-Type: application/json

{
  "username": "user1",
  "password": "password123"
}
```

Ответ содержит JWT-токен, который нужно использовать в заголовке `Authorization: Bearer <token>` для доступа к защищенным маршрутам.

### Управление задачами

Все маршруты задач требуют аутентификации.

#### Создание задачи
```bash
POST /api/tasks/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Купить продукты",
  "description": "Молоко, хлеб, яйца",
  "completed": false
}
```

#### Получение всех задач
```bash
GET /api/tasks/
Authorization: Bearer <your_token>
```

#### Получение задачи по ID
```bash
GET /api/tasks/{id}
Authorization: Bearer <your_token>
```

#### Обновление задачи
```bash
PUT /api/tasks/{id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Купить продукты",
  "description": "Молоко, хлеб, яйца, масло",
  "completed": true
}
```

#### Удаление задачи
```bash
DELETE /api/tasks/{id}
Authorization: Bearer <your_token>
```

## Модели данных

### Пользователь
- `id`: int (авто)
- `username`: str (уникальное, 1-100 символов)
- `email`: str (уникальный, валидный email)
- `password`: str (8-100 символов)
- `created_at`: datetime
- `updated_at`: datetime

### Задача
- `id`: int (авто)
- `title`: str (1-200 символов, обязательное)
- `description`: str (опционально)
- `completed`: bool (по умолчанию false)
- `user_id`: int (связь с пользователем)
- `created_at`: datetime
- `updated_at`: datetime

## Конфигурация

Параметры конфигурации задаются через переменные окружения в файле `.env`:

```env
ENV=local                # local или production
JWT_SECRET_KEY=secret    # Секретный ключ для JWT
POSTGRES_USER=postgres   # Пользователь PostgreSQL
POSTGRES_PASSWORD=postgres # Пароль PostgreSQL
POSTGRES_DB=db           # Название базы данных
POSTGRES_HOST=localhost  # Хост базы данных
```

## Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).
