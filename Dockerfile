FROM python:3.7-alpine

WORKDIR /bwm/bandwidth-monitor

COPY requirements.txt /bwm/requirements.txt
COPY bandwidth-monitor/ /bwm/bandwidth-monitor

RUN mkdir /bwm/data
RUN mkdir /bwm/log

RUN pip install -r /bwm/requirements.txt
RUN ln -sf /dev/stdout /bwm/log/bwm.log

ENTRYPOINT [ "python3", "main.py" ]