FROM python:3.13.7


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем исходный код
COPY . .



# Запуск приложения
# CMD ["python", "src/main.py"]

CMD alembic upgrade head; python src/main.py