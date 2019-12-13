FROM python:3.7-alpine

WORKDIR /bwm

COPY requirements.txt /bwm/requirements.txt
COPY bandwidth-monitor/ /bwm/bandwidth-monitor

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]