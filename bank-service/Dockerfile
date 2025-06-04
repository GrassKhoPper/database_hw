FROM ubuntu:latest

RUN rm /var/lib/apt/lists/* -fv
RUN apt update
RUN apt install -y \
	python3 \
	libssl-dev \
	python3-pip \
	python3-venv

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /bank
COPY . /bank

CMD ["uwsgi", "--ini", "uwsgi.ini"]

