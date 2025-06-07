# Dockerfile

# 1. Base Image
FROM python:3.9-slim-buster

# 2. Set Environment Variables
ENV PYTHONUNBUFFERED 1

# 3. Set Work Directory
WORKDIR /app

# 4. Copy and Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Copy Application Code
COPY . .

# 6. Expose Port
EXPOSE 8000

# 7. Run Command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]