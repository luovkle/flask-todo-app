FROM python:3.10

WORKDIR /todo-app

COPY ./requirements.txt /todo-app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /todo-app/app

CMD ["gunicorn", "app.run:app", "--bind", "0.0.0.0:8000"]
