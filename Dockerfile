FROM python:3.8-alpine

WORKDIR /bwm

COPY requirements.txt /bwm/requirements.txt
COPY config.ini /bwm/config.ini
COPY app/ /bwm/app

RUN pip install -r /bwm/requirements.txt

ENTRYPOINT [ "python3", "app/main.py" ]