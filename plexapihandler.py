import os
from plexapi.server import PlexServer
from plexapi.library import ShowSection, MovieSection
from plexapi.video import Movie, Episode


class PlexApiHandler(object):

    def __init__(self, baseurl, token):
        self.baseurl = baseurl
        self.plex = PlexServer(self.baseurl, token)

    def find_metadata_from_dirs(self, directories):
        """ finds all the metadata elements from directories """
        sections = self.plex.library.sections()
        result_set = []
        for section in sections:
            if isinstance(section, MovieSection):
                result_set.extend(self.process_movies(section, directories))
            if isinstance(section, ShowSection):
                result_set.extend(self.process_shows(section, directories))

        return result_set

    @staticmethod
    def file_path(full_path):
        head, tail = os.path.split(full_path)
        return head

    def process_shows(self, section: ShowSection, directories):
        library = section.all()
        result_set = []
        for element in library:
            for episode in element.episodes():
                for part in episode.iterParts():
                    if part.file in directories:
                        result_set.append(episode)

        return result_set

    def process_movies(self, section: MovieSection, directories):
        library = section.all()
        result_set = []
        for element in library:
            for part in element.iterParts():
                if PlexApiHandler.file_path(part.file) in directories:
                    result_set.append(element)
        return result_set

    def refresh_metadata(self, metadata_files):
        files_refreshed = []
        for element in metadata_files:
            element.refresh()
            files_refreshed.append(element.title)
        return files_refreshed
