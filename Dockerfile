# صورة Python رسمية
FROM python:3.11-slim

# إعداد مجلد العمل
WORKDIR /app

# تثبيت Poetry
RUN pip install poetry

# نسخ الملفات
COPY . .

# تثبيت التبعيات
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only main

# أمر التشغيل
CMD ["python", "src/main.py"]
