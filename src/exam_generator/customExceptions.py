class MissingDirectoryError(Exception):
    def __init__(self, info, file):
        self.info = info
        self.file = file


class MissingFileError(Exception):
    def __init__(self, info, file):
        self.info = info
        self.file = file


class SettingsError(Exception):
    def __init__(self, info, settings_file):
        self.info = info
        self.settings_file = settings_file


class CompilingError(Exception):
    def __init__(self, info):
        self.info = info
