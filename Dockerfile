FROM python:3.12

WORKDIR /product

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./code /product/code

EXPOSE 8080

CMD ["fastapi", "run", "code/app/main.py", "--port", "8080"]