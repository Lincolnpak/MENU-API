# Menu API

Небольшой REST API для управления меню ресторана. Написан на Flask, данные хранятся в SQLite.

## Возможности

- Получение списка блюд с фильтрацией по категории, максимальной цене и доступности
- Получение одного блюда по ID
- Добавление нового блюда
- Частичное обновление блюда (PATCH)
- Удаление блюда

## Стек

- Python 3.9+
- Flask
- SQLite (модуль `sqlite3` входит в стандартную библиотеку Python)

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/Lincolnpak/MENU-API
cd имя-репозитория
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте базу данных `menu.db` (один раз):

```bash
python -c "import sqlite3; c = sqlite3.connect('menu.db'); c.execute('''CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, available INTEGER NOT NULL DEFAULT 1)'''); c.commit(); c.close()"
```

Структура таблицы `dishes`:

| Поле        | Тип     | Описание                          |
|-------------|---------|-----------------------------------|
| `id`        | INTEGER | Первичный ключ, автоинкремент     |
| `name`      | TEXT    | Название блюда                    |
| `category`  | TEXT    | Категория (например, `main`)      |
| `price`     | REAL    | Цена                              |
| `available` | INTEGER | `1` — доступно, `0` — недоступно  |

5. Запустите приложение:

```bash
python app.py
```

Сервер стартует на `http://127.0.0.1:5000`.

## Эндпоинты

| Метод    | URL           | Описание                       |
|----------|---------------|--------------------------------|
| `GET`    | `/menu`       | Список блюд (с фильтрами)      |
| `GET`    | `/menu/<id>`  | Одно блюдо по ID               |
| `POST`   | `/menu`       | Добавить блюдо                 |
| `PATCH`  | `/menu/<id>`  | Обновить поля блюда            |
| `DELETE` | `/menu/<id>`  | Удалить блюдо                  |

### Фильтры для `GET /menu`

| Параметр    | Пример              | Описание                                   |
|-------------|---------------------|--------------------------------------------|
| `category`  | `?category=drink`   | Только блюда указанной категории           |
| `max_price` | `?max_price=30`     | Только блюда с ценой не выше указанной     |
| `available` | `?available=1`      | `1` — только доступные, `0` — недоступные  |

Фильтры можно комбинировать: `/menu?category=drink&max_price=10&available=1`

## Примеры запросов

Получить всё меню:

```bash
curl http://127.0.0.1:5000/menu
```

Добавить блюдо:

```bash
curl -X POST http://127.0.0.1:5000/menu \
  -H "Content-Type: application/json" \
  -d '{"name": "Плов", "category": "main", "price": 40}'
```

Ответ (`201 Created`):

```json
{
  "id": 1,
  "name": "Плов",
  "category": "main",
  "price": 40,
  "available": true
}
```

Изменить цену:

```bash
curl -X PATCH http://127.0.0.1:5000/menu/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 45}'
```

Удалить блюдо:

```bash
curl -X DELETE http://127.0.0.1:5000/menu/1
```

## Коды ответов

| Код   | Когда возвращается                                      |
|-------|---------------------------------------------------------|
| `200` | Успешный запрос                                         |
| `201` | Блюдо создано                                           |
| `400` | Некорректные данные или не переданы обязательные поля   |
| `404` | Блюдо не найдено                                        |

## Замечания

- Файл `menu.db` создаётся локально; добавьте его в `.gitignore`, если не хотите публиковать данные.
