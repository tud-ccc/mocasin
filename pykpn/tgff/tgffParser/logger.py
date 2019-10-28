# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

class IoColors():
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    SUCCESS = '\033[92m'
    ENDC = '\033[0m'
    
class Logger():
    def __init__(self, debug, silent):
        self.debug = debug
        self.silent = silent
    
    def log(self, message):
        if self.silent:
            return
        print(str(message))
    
    def logDebug(self, message):
        if self.silent:
            return
        if self.debug:
            print(str(message))
    
    def logError(self, message):
        print(IoColors.FAIL + str(message) + IoColors.ENDC)
    
    def logWarning(self, message):
        if self.silent:
            return
        print(IoColors.WARNING + str(message) + IoColors.ENDC)
    
    def logSuccess(self, message):
        print(IoColors.SUCCESS + str(message) + IoColors.ENDC)