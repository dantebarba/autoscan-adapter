import pathlib
from plexapi.server import PlexServer
from plexapi.library import ShowSection, MovieSection


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
            parts = len(pathlib.PurePath(location).parts)
            name = pathlib.PurePath(directory).parts[parts]

            if isinstance(section, MovieSection):
                return self.process_movies(section, directory, name)
            elif isinstance(section, ShowSection):
                return self.process_shows(section, directory, name)

    def process_shows(self, section: ShowSection, directory, show_name):
        library = section.search(show_name)
        result_set = []

        for element in library:
            for episode in element.episodes():
                for part in episode.iterParts():
                    if part.file.startswith(directory):
                        result_set.append(episode)

        return result_set

    def process_movies(self, section: MovieSection, directory, movie_name):
        library = section.search(movie_name)
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
