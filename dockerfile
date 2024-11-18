FROM python:3.10.0

WORKDIR /dcz

COPY ./requirements.txt /dcz/requirements.txt
RUN pip install --no-cache-dir -r /dcz/requirements.txt

RUN pip install python-dotenv

COPY .env /dcz/.env

COPY . /dcz/


EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]