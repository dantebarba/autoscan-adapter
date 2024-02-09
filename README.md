# Autoscan Plex Adapter

This app creates a bridge between [cloudb0x/autoscan](https://github.com/Cloudbox/autoscan) and Plex to enable metadata refresh. Works by mimicking an autoscan server. When the adapter receives the directories it connects to the plex instance and iterates all movies and episodes looking for a directory match. If a match is found the directory is added to the processing list and the metadata element gets refreshed in Plex.

**Disclaimer:** This app is WIP and has no authentication. Use it at your own risk.

## Installation

__tested under python 3.10__

```bash
pip install -r requirements.txt
```

## Usage

1. Create an `.env` file with the environment secrets

```bash
PLEX_URL=http://plex.domain.tld:32400
PLEX_TOKEN=YOUR-PLEX-TOKEN
ANALYZE_MEDIA="" # perform analysis of the media files after refresh. Empty or unset to disable
REFRESH_MEDIA="true" # perform metadata refresh of the media files. Active by default.
SLEEP_INTERVAL="0" # wait before starting the scanning process after each request. default is 0 (disabled)
LOG_LEVEL="INFO" # the logging level for the application. Available values are DEBUG, INFO, WARNING, ERROR. Default is INFO
```

2. Run the python flask server

```bash
python -m flask run -h 0.0.0.0
```

3. Add your autoscan adapter target to your autoscan config.yml

```yml
targets:
  plex:
    - url: http://plex:32400 # URL of your Plex server
      token: XXXX # Plex API Token
  autoscan:
    - url: http://autoscan-adapter:5000 # URL of your autoscan adapter
```

__By default flask runs on port 5000__

## Docker

This is a docker-compose.yml example. 

```yaml
version: '3.7'

services:
  autoscan:
    image: cloudb0x/autoscan
    container_name: autoscan
    restart: unless-stopped
    environment:
      PGID: $PGID
      PUID: $PUID
    volumes:
      - "./config:/config"
    depends_on:
      - autoscan-adapter

  autoscan-adapter:
    image: dantebarba/autoscan-adapter
    container_name: autoscan-adapter
    restart: unless-stopped
    environment:
      PGID: $PGID
      PUID: $PUID
      PLEX_URL: $PLEX_URL
      PLEX_TOKEN: $PLEX_TOKEN
      # perform analysis of the media files after refresh. empty or unset to disable. default: empty
      ANALYZE_MEDIA: $ANALYZE_MEDIA
      SLEEP_INTERVAL: $SLEEP
      REFRESH_MEDIA: $REFRESH_MEDIA
      LOG_LEVEL: $LOG_LEVEL
```

