"""this is just an example for a custom name processor"""


def preprocess_movie_directory(name: str):
    """process movie directory by replacing all dots and underscores with spaces

    Args:
        name (str): movie directory path
    """
    name = name.replace(".", " ").replace("_", " ")
    parts = name.split(" ")
    date_maybe = parts[-1]
    if date_maybe.startswith("(") and date_maybe.endswith(")"):
        return name.replace(date_maybe, "").rstrip()


def preprocess_show_directory(name: str):
    """this function receives a directory and returns the show name to be searched
    If you have radarr/sonarr file naming configured as default, leave it as is."""
    parts = name.split(" ")
    date_maybe = parts[-1]
    if date_maybe.startswith("(") and date_maybe.endswith(")"):
        return name.replace(date_maybe, "").rstrip()
