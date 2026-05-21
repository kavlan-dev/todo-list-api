FROM python:slim
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml README.md ./
COPY src/ src/

RUN poetry install

CMD ["poetry", "run", "python", "src/todo_list_api/main.py"]