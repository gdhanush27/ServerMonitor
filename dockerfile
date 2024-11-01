FROM python:3.12

WORKDIR /usr/src/app

ENV PORT=8000
ENV HOST=0.0.0.0

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${PORT}

CMD ["gunicorn", "app:app","$HOST:$PORT" ]