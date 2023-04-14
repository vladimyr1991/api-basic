FROM python:3.9
WORKDIR /app
COPY ./src /app
RUN apt-get update -y && \
    apt-get install -y
RUN pip install --user -r requirements.txt
EXPOSE 8000
CMD python api.py