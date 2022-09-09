from inspect import currentframe, getframeinfo

"""
This file contains custom errors for the exam generator.
"""


class MissingDirectoryError(Exception):
    """
    Error raised when a needed directory is missing.

    :param info: errorInfo()
    :type info: func

    :param directory: missing directory
    :type directory: str. Default None.
    """

    def __init__(self, info, directory=None):
        self.info = info
        self.file = directory


class MissingFileError(Exception):
    """
    Error raised when a needed file is missing.

    :param info: errorInfo()
    :type info: func

    :param file: missing file name
    :type file: str
    """

    def __init__(self, info, file=None):
        self.info = info
        self.file = file


class SettingsError(Exception):
    """
    Error raised when there is a problem with user input.

    :param info: errorInfo()
    :type info: func

    :param settings_file: name of settings file
    :type settings_file: str
    """

    def __init__(self, info, settings_file=None):
        self.info = info
        self.settings_file = settings_file


class CompilingError(Exception):
    """
    Error raised when there is a problem during the compiling process.

    :param info: errorInfo()
    :type info: func

    :param file: name of file where compiling failed
    :type file: str. Defaulted to None
    """

    def __init__(self, info, extra_info=None):
        self.info = info
        self.file = extra_info


def errorInfo():
    """
    Gives information about the origin of the raised error.

    :returns: Line of error + file
    :rtype: str
    """
    cf = currentframe()
    return f"Error in line {cf.f_back.f_lineno} in {getframeinfo(cf).filename}:"
