class NoKeyWordSupplied(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class LookupNotExecuted(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class TimeOutUbersuggest(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
