FROM python:3.9
WORKDIR /app
COPY ./src /app
RUN apt-get update -y && \
    apt-get install -y

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]