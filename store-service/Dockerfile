FROM python:3.12

WORKDIR /store

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /store

CMD ["python", "-u", "app.py"]

