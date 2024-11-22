FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --update --no-cache gcc libc-dev sqlite-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

