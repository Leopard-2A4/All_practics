FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируй requirements ПЕРВЫМ (кэшируется!)
COPY requirements.txt .

# Установи зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируй код ПОСЛЕДНИМ (часто меняется)
COPY . .

# Запуск
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]