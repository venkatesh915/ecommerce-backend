FROM python:3.12-slim

WORKDIR /app

# We don't have a requirements.txt yet, so let's install common ones
# In a real scenario, you'd COPY requirements.txt and pip install -r requirements.txt
RUN pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv psycopg2-binary passlib[bcrypt] python-jose python-multipart

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
