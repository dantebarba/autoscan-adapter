import pathlib
from plexapi.server import PlexServer
from plexapi.library import ShowSection, MovieSection


def name_without_date(name):
    parts = name.split(" ")
    date_maybe = parts[-1]
    if date_maybe.startswith("(") and date_maybe.endswith(")"):
        return name.replace(date_maybe, "").rstrip()


class PlexApiHandler(object):
    def __init__(self, baseurl, token):
        self.baseurl = baseurl
        self.plex = PlexServer(self.baseurl, token)

    def find_section_from_dirs(self, directory):
        sections = self.plex.library.sections()

        for section in sections:
            for location in section.locations:
                if directory.startswith(location):
                    return section, location

    def find_metadata_from_dirs(self, directory):
        """finds all the metadata elements from directories"""

        result = self.find_section_from_dirs(directory)
        if result:
            section, location = result
            section_parts = len(pathlib.PurePath(location).parts)
            media_name = pathlib.PurePath(directory).parts[section_parts]

            if isinstance(section, MovieSection):
                return self.process_movies(section, directory, media_name)
            elif isinstance(section, ShowSection):
                return self.process_shows(section, directory, media_name)

    def process_shows(self, section: ShowSection, directory, show_name):
        library = section.searchShows(title=show_name)

        # fall back to using the show name without date
        if not library:
            show_name_without_date = name_without_date(show_name)
            if show_name_without_date:
                library = section.searchShows(title=show_name_without_date)

        # fall back to searching the entire library (slowest)
        if not library:
            library = section.all()

        result_set = []

        for element in library:
            for episode in element.episodes():
                for part in episode.iterParts():
                    if part.file.startswith(directory):
                        result_set.append(episode)

        return result_set

    def process_movies(self, section: MovieSection, directory, movie_name):
        library = section.searchMovies(title=movie_name)

        # fall back to using the movie name without date
        if not library:
            movie_name_without_date = name_without_date(movie_name)
            if movie_name_without_date:
                library = section.searchMovies(title=movie_name_without_date)

        # fall back to searching the entire library (slowest)
        if not library:
            library = section.all()

        result_set = []

        for element in library:
            for part in element.iterParts():
                if part.file.startswith(directory):
                    result_set.append(element)

        return result_set

    def refresh_metadata(self, metadata_files):
        files_refreshed = []

        for element in metadata_files:
            element.refresh()
            files_refreshed.append(element.title)

        return files_refreshed
