FROM python:3.10.0

WORKDIR /dcz

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

ARG ACCESS_TOKEN_EXPIRES_MINUTES
ENV ACCESS_TOKEN_EXPIRES_MINUTES=${ACCESS_TOKEN_EXPIRES_MINUTES}

COPY ./requirements.txt /dcz/requirements.txt
RUN pip install --no-cache-dir -r /dcz/requirements.txt

RUN pip install python-dotenv
# RUN pip install --pre pyhwp

COPY . /dcz/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]