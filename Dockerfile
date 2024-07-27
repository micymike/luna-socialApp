FROM python:3.9

RUN useradd -m -u 1000 user

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt

RUN pip install -r requirements.txt && flask db upgrade

COPY --chown=user . /app

USER user

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
