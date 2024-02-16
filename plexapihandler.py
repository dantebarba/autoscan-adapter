import pathlib
from plexapi.server import PlexServer
from plexapi.library import ShowSection, MovieSection
from flask import current_app


class PlexApiHandler(object):
    def __init__(
        self, baseurl, token, moviename_processor_function, showname_processor_function
    ):
        """Plex API Handler functions

        Args:
            baseurl (_type_): The base URL to the PLEX instance. Schema should be included (http:// or https://)
            token (_type_): The PLEX instance token
            moviename_processor_function (func): the movie name processing function. By default matches the radarr standard config
            showname_processor_function (func): the show name processing function. By default matches the sonarr standard config
        """
        self.baseurl = baseurl
        self.plex = PlexServer(self.baseurl, token)
        self.moviename_processor = moviename_processor_function
        self.showname_processor = showname_processor_function

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
            section_parts_len = len(pathlib.PurePath(location).parts)
            directory_parts = pathlib.PurePath(directory).parts
            media_name = (
                pathlib.PurePath(directory).parts[section_parts_len]
                if section_parts_len < len(directory_parts)
                else ""
            )

            if isinstance(section, MovieSection):
                return self.process_movies(section, directory, media_name)
            elif isinstance(section, ShowSection):
                return self.process_shows(section, directory, media_name)

    def process_shows(self, section: ShowSection, directory, show_name):
        show_name_preprocessed = self.showname_processor(show_name)
        show_titles = "{},{}".format(show_name, show_name_preprocessed)
        library = section.searchShows(title=show_titles) or section.all()

        result_set = []

        for element in library:
            for episode in element.episodes():
                for part in episode.iterParts():
                    if part.file.startswith(directory):
                        result_set.append(episode)

        return result_set

    def process_movies(self, section: MovieSection, directory, movie_name):
        movie_name_without_date = self.moviename_processor(movie_name)
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
                    current_app.logger.debug(
                        f"Refreshing metadata of : {element.title}"
                    )
                    element.refresh()
                if also_analyze:
                    current_app.logger.debug(f"Analyzing element : {element.title}")
                    element.analyze()
                files_refreshed.append(element.title)

        return files_refreshed
