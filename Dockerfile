FROM python:2.7-onbuild

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 5000
