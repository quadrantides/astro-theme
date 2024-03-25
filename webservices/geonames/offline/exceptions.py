# coding=utf-8
"""
Created on 2020, Apr 3rd
@author: orion
"""


class CursorNotAvailable(Exception):
    def __init__(self, error):
        error_msg = "NO CURSOR AVAILABLE / DB ERROR : '{}'"
        Exception.__init__(
            self,
            error_msg.format(
                error,
            ),
        )
