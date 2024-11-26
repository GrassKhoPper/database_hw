FROM python:3.12

WORKDIR /bank

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /bank

CMD ["python", "app.py"]

