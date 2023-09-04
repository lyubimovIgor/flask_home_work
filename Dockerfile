# Используйте официальный образ Python
FROM python:3.10

# Установите переменные окружения
ENV PG_USER=postgres
ENV PG_PASSWORD=1986
ENV PG_DB=ads
ENV PG_HOST=db
ENV PG_PORT=5432

# Установите рабочую директорию
WORKDIR /app

# Копируйте зависимости и код в контейнер
COPY requirements.txt .
COPY app.py .
COPY models.py .

# Установите зависимости
RUN pip install -r requirements.txt

# Запустите приложение
CMD ["python", "app.py"]
