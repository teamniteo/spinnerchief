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