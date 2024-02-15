import os
import time

from flask import Blueprint
from flask import jsonify, request, current_app
from plexapihandler import PlexApiHandler

ENV_ANALYZE_MEDIA = os.getenv("ANALYZE_MEDIA", "")
ENV_REFRESH_MEDIA = os.getenv("REFRESH_MEDIA", "true")

main_bp = Blueprint('main', __name__)
sleep = int(os.getenv("SLEEP_INTERVAL", "0"))
plex_api = PlexApiHandler(os.getenv("PLEX_URL"), os.getenv("PLEX_TOKEN"))


@main_bp.route("/")
def ping():
    return "Ping successful"

@main_bp.route("/triggers/manual", methods=["HEAD"])
def ok():
    return "Ok"

@main_bp.route("/triggers/manual", methods=["POST", "GET"])
def trigger():
    directories = request.args.getlist("dir")

    if sleep:
        time.sleep(sleep)
    
    current_app.logger.warning("Starting directory scan of: {}".format(directories))

    metadata_entries = []

    if directories:
        for directory in directories:
            metadata_files = plex_api.find_metadata_from_dirs(directory=directory)
            files_refreshed = plex_api.refresh_metadata(metadata_files, ENV_ANALYZE_MEDIA, ENV_REFRESH_MEDIA)
            metadata_entries.extend(files_refreshed)
    
    return jsonify(metadata_entries=metadata_entries)
