FROM python:3.10-slim

RUN mkdir -m 777 /app

RUN pip install poetry==1.4.1
COPY poetry.lock pyproject.toml .env /app/

WORKDIR /app/

COPY /src/* /app/

RUN poetry --no-root install

ENTRYPOINT ["poetry", "run", "python3.10", "main.py"]
