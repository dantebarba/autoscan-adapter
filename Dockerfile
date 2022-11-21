FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV PLEX_URL ""
ENV PLEX_TOKEN ""

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
