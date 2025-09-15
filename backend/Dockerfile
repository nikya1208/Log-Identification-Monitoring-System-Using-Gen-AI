# backend/Dockerfile

# ✅ Use official Python image
FROM python:3.12

WORKDIR /app

# ✅ Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy project files
COPY . .

# ✅ Expose application port
EXPOSE 8000

# ✅ Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
