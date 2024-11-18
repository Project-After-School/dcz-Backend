FROM python:3.10.0

WORKDIR /dcz

COPY ./requirements.txt /dcz/requirements.txt

RUN pip install --no-cache-dir -r /dcz/requirements.txt

COPY . /dcz/

ENV DATABASE_URL=${DATABASE_URL}
ENV SECRET_KEY=${SECRET_KEY}
ENV ACCESS_TOKEN_EXPIRES_MINUTES=${ACCESS_TOKEN_EXPIRES_MINUTES}

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
