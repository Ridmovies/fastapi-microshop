# Название Проекта

Краткое описание проекта.

## Описание

Подробнее о проекте, его целях и функциональности.

## Инструменты в проекте:
* FastApi
* Poetry


## Установка

Запустить проект
```bash
uvicorn main:app --reload

```

### Требования

Список необходимых зависимостей и программного обеспечения.

### Установка зависимостей

Команды для установки зависимостей.

### Настройка

Шаги для настройки проекта перед запуском.

## Запуск

Инструкции по запуску проекта.

### Локальный запуск

Команды для запуска проекта локально.

### Развертывание

Рекомендации по развертыванию проекта в продакшн-среду.

## Документация

Ссылки на документацию API и другие полезные ресурсы.

## Лицензия

Информация о лицензии проекта.

## Контакты

Контактная информация для связи с автором или командой проекта.


## Разработка

### Alembic

### Создайте директорию для хранения конфигурационных файлов и скриптов миграции:
```bash
alembic init -t async alembic
```

### Генерация первой миграции
```bash
alembic revision --autogenerate -m "initial migration"
```

### Примените созданную миграцию к базе данных:
```bash
alembic upgrade head
```

### Poetry Система контроля зависимостей
### Создание нового проекта

```Bash
poetry new my-project
```
Эта команда создаст новую структуру проекта с файлом pyproject.toml, где будут храниться зависимости.

### Инициализация существующего проекта

```Bash
poetry init
```
Эта команда инициализирует проект, задавая необходимые параметры и создавая файл pyproject.toml.

### Добавление пакета

```Bash

poetry add requests
```
Добавляет пакет requests в список зависимостей вашего проекта.
Чтобы добавить пакет в секцию [tool.poetry.dev-dependencies] файла pyproject.toml, нужно использовать следующую команду:

```Bash
poetry add <package-name> --group dev
```

### Обновление всех пакетов

```Bash
poetry update
```
Обновляет все пакеты до последних совместимых версий.


### Синхронизация poetry с виртуальным окружением
```Bash
poetry install --sync
```


### Показать дерево пакетов
```Bash
poetry show --tree
```

### Для удаления пакета
```Bash
   poetry remove <имя_пакета>
```

## Линтеры и форматеры:
```bash
black --check --diff --color ./app/booking/services.py
```

```bash
isort --check-only --diff --profile black ./app/booking/services.py
```

```bash
mypy --incremental ./product_app/views.py 
```

```bash
autoflake ./app/booking/router.py
```

```bash
pyright .
```


## Полезные материалы:

### Репозиторий оригинала
https://github.com/mahenzon/micro-shop

### FastAPI Best Practices 
https://github.com/zhanymkanov/fastapi-best-practices

