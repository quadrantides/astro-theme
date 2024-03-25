"""
List of applicative exceptions

"""

"""
Configuration exceptions
(bad entries in development.ini or production.ini files)

"""


class ConfigSectionNotFound(Exception):
    def __init__(self, name, full_filename):
        error_msg = "Requested section : '{}' not found in the '{}' Config FILE"
        Exception.__init__(
            self,
            error_msg.format(
                name,
                full_filename,
            ),
        )


class ConfigError(Exception):

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return repr(self.value)
