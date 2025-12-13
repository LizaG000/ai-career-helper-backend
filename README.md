Базовый проект FastAPI
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

⚙️ Требования
Перед запуском убедись, что установлены:

   [Python 3.11+](https://www.python.org/)
   
   [Docker](https://www.docker.com/products/docker-desktop/)
   
------------------------------------------------------------------------------------------------------------
  
📦 Как запустить проект
1. Склонируйте проект
   ```
   git clone https://github.com/LizaG000/ai-career-helper-backend.git
   cd ai-career-helper-backend
   ```

3. Создайте файл окружения config.toml
   ```
   cd deploy
   cp configs/excemple.config.toml configs/config.toml 
   ```
4. Создайте и запустите виртуальное окружение
   ```
   python -m venv [имя_вашего_окружения]
   ```
   Запуск для Windows
   ```
   [имя_вашего_окружения]\Scripts\activate
   ```
   Запуск для Linux и MacOS
   ```
   source [имя_вашего_окружения]/bin/activate
   ```
5. Установка зависимостей
   ```
   pip install makefile poetry
   poetry install
   ```
6. Проверьте, что у вас есть bash

   Для Windows
   
   - Вариант 1: Использование подсистемы Windows для Linux (WSL)
      - Откройте PowerShell от имени администратора
      ```
      wsl --install
      ```
      - Перезагрузите компьютер
      - Откройте Ubuntu из меню «Пуск»
      - Вам будет предложено создать имя пользователя и пароль для среды Linux
   - Вариант 2: Использование Git Bash
      - Перейдите на официальный [сайт](gitforwindows.org) Git для Windows
      - Загрузите установочный файл
      - Запустите загруженный .exe и следуйте инструкциям на экране
      - В процессе установки выберите использование Git Bash
      - После завершения установки вы сможете запустить Git Bash через меню «Пуск».
   
   Для Linux (чаще всего установлен по умолчанию)
   
   Чтобы проверить
   ```
   bash --version
   ```
   
   Чтобы установить
   - Ubuntu или Debian:
     ```
     sudo apt-get install bash.
     ```
   - Fedora или CentOS:
     ```
     sudo dnf install bash.
     ```

   Для MacOS (чаще всего установлен по умолчанию)
   
   Чтобы проверить
   ```
   bash --version
   ```
   
   Чтобы установить
   ```
   brew install bash
   ```

7. Вернуться в корень проекта и запустить через Makefile (если у вас виндовс просто дублируйте команды)
   ```
   cd ..
   make compose
   ```

8.  После запуска открой в браузере:
   
     http://localhost:8000/docs

9. Чтобы остановить проект
   ```
   make down
   ```

------------------------------------------------------------------------------------------------------------

Очередь задач (TaskIQ)

- Убедись, что в `deploy/configs/config.toml` есть блок `redis` (по умолчанию `host=redis`, `port=6379`, `db=0` из docker-compose).
- При `make compose` поднимается отдельный контейнер `taskiq-worker`, который сам запускает воркер очереди.
- Локально без Docker можно запустить воркер вручную (из корня репозитория):
  ```
  poetry run taskiq worker src.infra.taskiq.tasks:broker
  ```
- Ручка для постановки задач: `POST /api/cards/tasks` со следующей формой запроса:
  - `usecase`: один из `create_cards`, `update_card`, `delete_card`, `generate_cards`, `get_all_cards`
  - `payload`: параметры для выбранного юзкейса.
- Примеры запросов:
  - Создание карточек
    ```
    {
      "usecase": "create_cards",
      "payload": {
        "cards": [
          {
            "information_title": "Python",
            "title": "PEP 8",
            "description": "Style guide."
          }
        ]
      }
    }
    ```
  - Удаление карточки
    ```
    {
      "usecase": "delete_card",
      "payload": { "id": "uuid-card-id" }
    }
    ```
  - Генерация предзагруженных карточек
    ```
    { "usecase": "generate_cards" }
    ```

------------------------------------------------------------------------------------------------------------

❗️ Как отправлять Pull Request 

1. Клонируем репозиторий
   
Если ты ещё не скачивал проект:
```
git clone https://github.com/LizaG000/ai-career-helper-backend.git
cd ai-career-helper-backend
```

2. Создаём новую ветку

Перед началом работы никогда не коммить в main.

Создай отдельную ветку для своей задачи:
```
git checkout -b feature/task-name
```

Примеры названий веток:

- /add-tasks-api

- fix/user-validation

- docs/update-readme
  

3. Работаем над задачей

Делаем нужные изменения, коммитим их.
```
git add .
git commit -m "Добавил эндпоинт для создания задач"
```

4. Отправляем ветку в GitHub
   ```
   git push origin feature/task-name
   ```
5. Создаём Pull Request
   - Открой репозиторий на GitHub.

   - GitHub предложит “Compare & pull request” — нажми на него.

   - Проверь, что:

      - Base branch → main

      - Compare branch → твоя feature/task-name

   - Добавь описание:

      - Что сделано

      - Какие файлы/модули изменены

      - Что нужно проверить (если есть)
        

5. Нажми “Create Pull Request” ✅

   
------------------------------------------------------------------------------------------------------------

👀 Команды Makefile

make compose - Собрать и запустить проект + применить миграции

make down - Остановить и удалить контейнеры

make migrations_init	- Создать первую миграцию Alembic

make makemigrations MSG="add new table" - Создать новую миграцию с сообщением

make migrate - Применить все миграции

make downgrade - Откатить последнюю миграцию

------------------------------------------------------------------------------------------------------------

🧠 Как устроен проект

src/

├── application/   # Модели, схемы и ошибки

├── infra/         # Работа с базой данных и миграции + внешние сервисы

├── main/          # Запуск приложения, DI-контейнер

├── presentation/  # FastAPI (роуты, хэндлеры)

├── usecase/       # Бизнес-логика (создание, получение и т.п.)

└── config.py      # Основные настройки

------------------------------------------------------------------------------------------------------------

✌️ Пример как с этим работать

- Запустили проект

- Добавим новую сущность (tasks)
  
  Напишем схему в файл src/application/schemas/tasks.py

```
from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class TaskSchema(BaseModel):
    id: UUID
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime

class CreateTaskSchema(BaseModel):
    title: str
    description: str | None = None
```

- Добавим таблицу в базу
  
  В src/infra/postgres/tables.py
  
```
class TaskModel(BaseDBModel):
    __tablename__ = 'tasks' 
    id: Mapped[uuid_pk] 
    title: Mapped[str] = mapped_column(String(255), nullable=False) 
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
```

- Создадим миграцию и применим её
  ```
  make makemigrations MSG="add task model"
  make migrate
  ```
  
- Добавим usecase (логику)
  
  в src/usecase/tasks/create.py
  
```
from src.application.schemas.tasks import TaskSchema, CreateTaskSchema
from src.infra.postgres.tables import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.gateways.base import CreateReturningGate
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateTaskUsecase(Usecase[CreateTaskSchema, TaskSchema]):
    """Usecase для создания новой задачи"""
    session: AsyncSession
    create_user: CreateReturningGate[TaskModel, CreateTaskSchema, TaskSchema]

    async def __call__(self, task: CreateTaskSchema) -> TaskSchema:
        async with self.session.begin():
            return await self.create_task(task)
```

  в src/usecase/tasks/get_all.py

```
from src.application.schemas.tasks import TaskSchema
from src.infra.postgres.tables import TaskModel
from src.infra.postgres.provider import Session
from sqlalchemy import select


class GetTasksUsecase:
    """Usecase для получения списка задач"""

    def __init__(self, session: Session):
        self.session = session

    async def __call__(self) -> list[TaskSchema]:
        result = await self.session.execute(select(TaskModel))
        tasks = result.scalars().all()
        return [TaskSchema.model_validate(task) for task in tasks]
```

- Создадим API-роут
  
  в src/presentation/fastapi/routes/core/tasks/api.py
```
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from src.application.schemas.tasks import CreateTaskSchema, TaskSchema
from src.usecase.tasks.create import CreateTaskUsecase
from src.usecase.tasks.get_all import GetTasksUsecase

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_tasks(usecase: FromDishka[GetTasksUsecase]) -> list[TaskSchema]:
    return await usecase()


@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_task(
    usecase: FromDishka[CreateTaskUsecase],
    task: CreateTaskSchema
) -> TaskSchema:
    return await usecase(task)

```
  
  И зарегистрируем роут в src/presentation/fastapi/routes/core/setup.py
  
```
from src.presentation.fastapi.routes.core.tasks.api import ROUTER as TASK_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/user', router=USER_ROUTER)
    router.include_router(prefix='/task', router=TASK_ROUTER)
    return router

```

   Добавляем наши юзкейсы в /Users/mac/AI-furniture-bot/backend/src/main/provider.py

```
_get_usecases = provide_all(
   CreateTaskUsecase,
   GetTasksUsecase,
    )
```

- Проверяем результат
  
  Обновляем страницу Сваггера

- Видим, что появился новый раздел Tasks
  
- ТЫ УМНИЧКААААААААААААААААА 🎉
  
