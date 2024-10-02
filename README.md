# test-task-cats
## Команды для запуска проекта

1. **Создание виртуального окружения**:
    ```bash
    python -m venv .venv
    ```

2. **Активация виртуального окружения**:
    - Для Linux/MacOS:
      ```bash
      source .venv/bin/activate
      ```
    - Для Windows:
      ```bash
      .venv\Scripts\activate
      ```

3. **Установка зависимостей проекта**:
    ```bash
    pip install -r requirements.txt
    ```
   
4. **Применение миграций**:
   ```bash
   python manage.py runserver
   ```

5. **Запуск проекта**:
   ```bash
   python manage.py runserver
   ```
   
6. **Если нужно отформатировать код, то можно прогнать все линтеры**:
   ```bash
   pre-commit run -a
   ```

## Запуск проекта с помощью Docker
   ```bash
    docker-compose up --build 
   ```