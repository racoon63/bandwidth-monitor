FROM python:3.7-alpine

WORKDIR /bwm

COPY requirements.txt /bwm/requirements.txt
COPY bwm /bwm/bwm
COPY lib/ /bwm/lib
COPY config.ini /bwm/config.ini

RUN pip install -r /bwm/requirements.txt

ENTRYPOINT [ "python3", "bwm" ]