import os
from flask import Flask, jsonify, request, current_app
from plexapihandler import PlexApiHandler

app = Flask(__name__)
plex_api = PlexApiHandler(os.getenv("PLEX_URL"), os.getenv("PLEX_TOKEN"))


@app.route("/")
def ping():
    return "Ping successfull"


@app.route("/triggers/manual", methods=["POST", "GET", "HEAD"])
def manual_trigger():
    directory = request.args.get("dir")
    current_app.logger.warning("Starting directory scan of: {}".format(directory))

    if directory:
        metadata_files = plex_api.find_metadata_from_dirs(directory=directory)
        files_refreshed = plex_api.refresh_metadata(metadata_files)
        return jsonify(metadata_entries=files_refreshed)

    return jsonify(metadata_files=[])
