# This file defines the context class
#
#Author: Robert Khasanov


class Context(object):
    """A singleton class for keeping `static` objects in one place.

    Attributes:
        req_table (ReqTable): Request table
        app_table (AppTable): Application table
    """
    __instance = None

    def __new__(cls):
        if Context.__instance is None:
            Context.__instance = object.__new__(cls)
            Context.__instance.__init()
        return Context.__instance

    def __init(self):
        self.req_table = None
