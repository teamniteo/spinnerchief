# -*- coding: utf-8 -*-

import urllib
import urllib2
import base64

from spinnerchief import exceptions as ex


class SpinnerChief(object):
    """A class representing the Spinner Chief API
    (http://developer.spinnerchief.com/API_Document.aspx).
    """
    URL = u'http://api.spinnerchief.com:9001/apikey=%s&username=%s&password=%s&'
    """URL for invoking the API"""

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
        self._url = self.URL % (apikey, username, password)

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

        if params == None:
            params = self.DEFAULT_PARAMS

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

        if params == None:
            params = self.DEFAULT_PARAMS

        params['spintype'] = '1'

        return self._send_request(text=text, params=params)

    def _send_request(self, text='', params=DEFAULT_PARAMS):
        """ Invoke Spinner Chief API with given parameters and return its response .

        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: API's response (article)
        :rtype: string
        """

        # remove entries with None value
        temp = dict([(i,j) for i,j in params.iteritems() if j!=None])

        urldata = self._url + urllib.urlencode(temp)
        base64text = base64.b64encode(text)
        req = urllib2.Request(urldata, data=base64text)
        response = urllib2.urlopen(req)

        result = base64.b64decode(response.read())

        if result.lower().startswith('error='):
            self._raise_error(result[6:])

        return result

    def _raise_error(self, api_response):
        lower = api_response.lower()
        error = None

        if lower.startswith("login error"):
            error = ex.LoginError(api_response)

        raise error if error else ex.SpinnerChiefError(api_response)
