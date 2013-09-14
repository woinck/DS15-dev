# -*- coding: UTF-8 -*-

#
#error module
#ver 1.0 edited at 2013-08-12-22:47
#

import exceptions

class Ui_Error(exceptions.Exception):
    def __init__(self, name, _dir, note, *args, **argv):
        exceptions.Exception.__init__(self, *args)
        self.name = name
        self.dir = _dir
        self.note = note
        for attr in argv.keys():
            self.__setattr__(attr, argv[attr])

    def __str__(self):
        message = "\n" +self.name+": "
        message += "\nError in "
        for i in self.dir:
            message = message+i+", "
        message = message+"\n"+self.note+"\n"
        return message

        
