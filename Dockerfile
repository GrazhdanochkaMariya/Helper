FROM python:3.11-slim

WORKDIR /opt/app/

COPY ./requirements.txt /opt/app/

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install -r /opt/app/requirements.txt

COPY . /opt/app/

CMD alembic upgrade head && uvicorn main:app --host=0.0.0.0 --port 80 --reload
