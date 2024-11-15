FROM python:3.12-alpine

WORKDIR /store

COPY requirements.txt .

RUN apk add --update --no-cache gcc libc-dev sqlite-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /store
VOLUME /store

ENV PYTHONPATH "${PYTHONPATH}:/"
CMD ["python", "-m", "store"]

