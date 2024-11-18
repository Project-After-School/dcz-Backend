FROM python:3.10.0


WORKDIR /dcz

COPY ./requirements.txt /dcz/requirements.txt


RUN pip install --no-cache-dir -r /dcz/requirements.txt

RUN apt-get update && apt-get install -y bash && apt-get clean
RUN cat .env | grep -v '^#' | xargs -d '\n' -I {} bash -c 'export {}'
COPY . /dcz/

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
