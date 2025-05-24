FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

RUN chmod -R 777 /app

EXPOSE 5000
CMD ["python", "app.py"]
