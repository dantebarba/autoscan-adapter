FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV PLEX_URL ""
ENV PLEX_TOKEN ""
ENV ANALYZE_MEDIA ""
ENV REFRESH_MEDIA "true"
ENV LOG_LEVEL "INFO"
ENV SLEEP_INTERVAL "0"
ENV DIRECTORY_PROC_MODULE "nameprocessor"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
