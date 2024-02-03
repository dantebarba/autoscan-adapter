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
        show_name_without_date = name_without_date(show_name)
        show_titles = "{},{}".format(show_name, show_name_without_date)
        library = section.searchShows(title=show_titles) or section.all()

        result_set = []

        for element in library:
            for episode in element.episodes():
                for part in episode.iterParts():
                    if part.file.startswith(directory):
                        result_set.append(episode)

        return result_set

    def process_movies(self, section: MovieSection, directory, movie_name):
        movie_name_without_date = name_without_date(movie_name)
        movie_titles = "{},{}".format(movie_name, movie_name_without_date)
        library = section.searchMovies(title=movie_titles) or section.all()

        result_set = []

        for element in library:
            for part in element.iterParts():
                if part.file.startswith(directory):
                    result_set.append(element)

        return result_set

    def refresh_metadata(self, metadata_files, also_analyze="", also_refresh="true"):
        files_refreshed = []

        if metadata_files:
            for element in metadata_files:
                if also_refresh:
                    element.refresh()
                if also_analyze:
                    element.analyze()
                files_refreshed.append(element.title)

        return files_refreshed
