from datetime import datetime


class Logger:
  className = None

  def __init__(self, className):
    self.className = className

  def info(self, message, *args):
    self.__log__(colors.OKGREEN, "INFO", message, args)

  def warn(self, message, *args):
    self.__log__(colors.WARNING, "WARN", message, args)

  def error(self, message, *args):
    self.__log__(colors.FAIL, "ERROR", message, args)

  def __log__(self, color, level, message, args):
    print(color + "[{0}][JTALKS][{1}][{2}] ".format(datetime.now().isoformat(), level, self.className) +
          message.format(*args) + colors.END)


class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  END = '\033[0m'

  def disable(self):
    self.HEADER = ''
    self.OKBLUE = ''
    self.OKGREEN = ''
    self.WARNING = ''
    self.FAIL = ''
    self.ENDC = ''
