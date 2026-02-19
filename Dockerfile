FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip instal -r requirements.txt
COPY . .
CMD ["python", "main.py"]
