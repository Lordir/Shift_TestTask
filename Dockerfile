FROM python:3.9.5

WORKDIR /fastapi_app

# RUN pip install poetry

# COPY pyproject.toml /fastapi_app
COPY requirements.txt /fastapi_app

# RUN poetry install --no-root
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host=0.0.0.0 --port=8000