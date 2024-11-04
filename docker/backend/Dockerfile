FROM python:3.12.4
WORKDIR /backend

COPY /docker/backend/requirements.text .
RUN pip install --no-cache-dir  --upgrade -r /backend/requirements.text

COPY main.py /backend/
COPY /back .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]