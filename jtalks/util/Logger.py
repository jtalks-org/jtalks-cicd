from datetime import datetime


class Logger:
    class_name = None

    def __init__(self, class_name):
        self.class_name = class_name

    def info(self, message, *args):
        self.__log__(colors.OKGREEN, "INFO", message, args)

    def warn(self, message, *args):
        self.__log__(colors.WARNING, "WARN", message, args)

    def error(self, message, *args):
        self.__log__(colors.FAIL, "ERROR", message, args)

    def __log__(self, color, level, message, args):
        print(color + "[{0}][JTALKS][{1}][{2}] ".format(datetime.now().isoformat(), level, self.class_name) +
              message.format(*args) + colors.END)


class colors:
    HEADER = '\033[35m'
    OKBLUE = '\033[34m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    END = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
