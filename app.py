import os
from flask import Flask, jsonify, request
from plexapihandler import PlexApiHandler

app = Flask(__name__)
plex_api = PlexApiHandler(os.getenv("PLEX_URL"), os.getenv("PLEX_TOKEN"))


@app.route("/")
def ping():
    return "Ping successfull"


@app.route("/triggers/manual", methods=["POST"])
def manual_trigger():
    directories = request.args.getlist('dir')
    if directories:
        metadata_files = plex_api.find_metadata_from_dirs(
            directories=directories)
        files_refreshed = plex_api.refresh_metadata(metadata_files)
        return jsonify(
            metadata_entries=files_refreshed
        )
    return jsonify(
        metadata_files=[]
    )
