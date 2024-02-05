import os
import time

from flask import Flask, jsonify, request, current_app
from plexapihandler import PlexApiHandler

ENV_ANALYZE_MEDIA = os.getenv("ANALYZE_MEDIA", "")
ENV_REFRESH_MEDIA = os.getenv("REFRESH_MEDIA", "true")
ENV_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

app = Flask(__name__)
app.logger.setLevel(ENV_LOG_LEVEL)
sleep = int(os.getenv("SLEEP_INTERVAL", "0"))
plex_api = PlexApiHandler(os.getenv("PLEX_URL"), os.getenv("PLEX_TOKEN"))


@app.route("/")
def ping():
    return "Ping successful"

@app.route("/triggers/manual", methods=["HEAD"])
def ok():
    return "Ok"

@app.route("/triggers/manual", methods=["POST", "GET"])
def trigger():
    directory = request.args.get("dir")

    if sleep:
        time.sleep(sleep)
    
    current_app.logger.warning("Starting directory scan of: {}".format(directory))

    if directory:
        metadata_files = plex_api.find_metadata_from_dirs(directory=directory)
        files_refreshed = plex_api.refresh_metadata(metadata_files, ENV_ANALYZE_MEDIA, ENV_REFRESH_MEDIA)
        return jsonify(metadata_entries=files_refreshed)
    return jsonify(metadata_files=[])
