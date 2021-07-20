FROM python:3.8-slim

WORKDIR /getMacAddr

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "get_mac_addr.py" ]