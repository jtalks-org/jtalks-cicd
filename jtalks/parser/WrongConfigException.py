class WrongConfigException(Exception):
    def __init__(self, message):
        self.value = message

    def __str__(self):
        return repr(self.value)
