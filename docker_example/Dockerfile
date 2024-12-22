# Use a smaller base image with Python and pip
FROM python:3.11-slim

WORKDIR /app

COPY classifier/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir virtualenv

RUN virtualenv /venv && \
    /venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY classifier/ /app/

ENV PATH="/venv/bin:$PATH"

EXPOSE 9995

CMD sh -c "rq worker classifier_rest_api --path /app & flask run --host=0.0.0.0 --port=9995"
