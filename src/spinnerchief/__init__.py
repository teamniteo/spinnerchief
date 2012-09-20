# -*- coding: utf-8 -*-

import urllib
import urllib2
import base64
from sets import Set

from spinnerchief import exceptions as ex


class SpinnerChief(object):
    """A class representing the Spinner Chief API
    (http://developer.spinnerchief.com/API_Document.aspx).

    Articles must be in Unicode object type.
    """
    URL = u'http://api.spinnerchief.com:9001/apikey={apikey}&username={username}&password={password}&'
    """URL for invoking the API"""

    TIMEOUT = 10

    DEFAULT_PARAMS = {
        'protecthtml': '0',
        'usehurricane': '1',
        'spinhtml': '0',
        'percent': '0',
        'phrasecount': '2',
        'Chartype': '1',
        'replacetype': '0',
        'autospin': '1',
        'convertbase': '0',
        'thesaurus': 'English',
        'pos': '0',
        'Orderly': '0',
        'Wordscount': '5',
        'spinfreq': '4',
        'tagprotect': '[]',
        'spintype': '0',
        'UseGrammarAI': '0',
        'protectwords': None,
        'rule': 'none',
        'onecharforword': '0',
        'wordquality': '0',
        'original': '0',
    }

    def __init__(self, apikey, username, password):
        self._url = self.URL.format(apikey=apikey, username=username, password=password)

    def _get_param_value(self, param_name, params):
        """ Returns parameter value or use default.
        """
        if param_name in params:
            return params[param_name]

        elif param_name in self.DEFAULT_PARAMS:
            return self.DEFAULT_PARAMS[param_name]

        else:
            raise ex.WrongParameterName(param_name)

    def _value_has(self, param, values, params):
        """ Raise WrongParameterVal if
        value of param is not in values.
        """
        val = self._get_param_value(param, params)
        if not val in values:
            raise ex.WrongParameterVal(param, val)

    def _value_is_int(self, param, params):
        """ Raise WrongParameterVal if
        value of param is not integer.
        """
        val = self._get_param_value(param, params)
        try:
            int(val)
        except ValueError:
            raise ex.WrongParameterVal(param, val)

    def _validate(self, params):
        """ Checks every single parameter and
        raise error on wrong key or value.
        """
        # remove entries with None value
        for i, j in params.iteritems():
            if j is None:
                del(i)

        self._value_has('protecthtml', ['0', '1'], params)

        self._value_has('usehurricane', ['0', '1'], params)

        self._value_has('spinhtml', ['0', '1'], params)

        self._value_has('percent', map(lambda x: str(x), range(0, 101)), params)

        self._value_has('phrasecount', ['2', '3', '4', 'X'], params)

        self._value_has('Chartype', ['1', '2', '3'], params)

        self._value_has('replacetype', map(lambda x: str(x), range(0, 6)), params)

        self._value_has('autospin', ['0', '1'], params)

        self._value_has('convertbase', ['0', '1'], params)

        self._value_has('pos', ['0', '1'], params)

        self._value_has('Orderly', ['0', '1'], params)

        self._value_is_int('Wordscount', params)

        self._value_is_int('spinfreq', params)

        # allow any combination of '[]','()','<-->'
        val = self._get_param_value('tagprotect', params)
        if Set(val.split(',')).difference(Set(['[]', '()', '<-->'])):
            raise ex.WrongParameterVal('tagprotect', val)

        self._value_has('spintype', ['0', '1'], params)

        self._value_has('UseGrammarAI', ['0', '1'], params)

        self._value_has('onecharforword', ['0', '1'], params)

        self._value_has('wordquality', ['0', '1', '2', '3', '9'], params)

        self._value_has('original', ['0', '1'], params)

        return True

    def quota_used(self):
        """ The server returns today's used query times of this account.
        """
        response = self._send_request(text='', params={'querytimes': 1})
        return response

    def quota_left(self):
        """ The server returns today's remaining query times of this account.
        """
        response = self._send_request(text='', params={'querytimes': 2})
        return response

    def text_with_spintax(self, text, params=None):
        """ Return processed spun text with spintax.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text in spintax format
        :rtype: string
        """

        if params is None:
            params = self.DEFAULT_PARAMS
        else:
            self._validate(params)

        params['spintype'] = '0'

        return self._send_request(text=text, params=params)

    def unique_variation(self, text, params=None):
        """ Return a unique variation of the given text.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text
        :rtype: string
        """

        if params is None:
            params = self.DEFAULT_PARAMS
        else:
            self._validate(params)

        params['spintype'] = '1'

        return self._send_request(text=text, params=params)

    def _send_request(self, text='', params=DEFAULT_PARAMS):
        """ Invoke Spinner Chief API with given parameters and return its response.

        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: API's response (article)
        :rtype: string
        """

        urldata = self._url + urllib.urlencode(params)
        base64text = base64.b64encode(text.encode("utf-8"))
        req = urllib2.Request(urldata, data=base64text)
        try:
            response = urllib2.urlopen(req, timeout=self.TIMEOUT)
        except urllib2.URLError as e:
            raise ex.NetworkError(str(e))

        result = base64.b64decode(response.read()).decode("utf-8")

        if result.lower().startswith('error='):
            self._raise_error(result[6:])

        return result

    def _raise_error(self, api_response):
        lower = api_response.lower()
        error = None

        if lower.startswith("login error"):
            error = ex.LoginError(api_response)

        raise error if error else ex.SpinnerChiefError(api_response)
