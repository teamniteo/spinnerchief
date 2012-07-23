# -*- coding: utf-8 -*-


class SpinnerChiefError(Exception):
    """Base class for exceptions in Spinner Chief module."""
    def __init__(self, api_error_msg):
        #api_error_msg respresents raw error string as returned by API server
        super(SpinnerChiefError, self).__init__()
        self.api_error_msg = api_error_msg

    def __str__(self):
        return self.api_error_msg


class LoginError(SpinnerChiefError):
    def __str__(self):
        return self.api_error_msg


class WrongParameterName(SpinnerChiefError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return u"Parameter '%s' does not exist." % self.name


class WrongParameterVal(SpinnerChiefError):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __str__(self):
        return u"Parameter '%s' has a wrong value: '%s'" % (self.name, self.val)


class NetworkError(SpinnerChiefError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
