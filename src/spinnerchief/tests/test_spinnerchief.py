# -*- coding: utf-8 -*-

import base64
from spinnerchief import SpinnerChief

import unittest2 as unittest
import mock


class TestApi(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.sc = SpinnerChief('test_api_key', 'foo@bar.com', 'test_password')

    def test_init(self):
        """Test initialization of SpinnerChief.

        SpinnerChief is initialized on every test run and stored as self.sc.
        We need to test for stored values if class was
        initialized correctly.
        """
        self.assertEquals(
            self.sc._url,
            self.sc.URL.format(
                apikey='test_api_key',
                username='foo@bar.com',
                password='test_password'
            )
        )
        self.assertIsInstance(self.sc, SpinnerChief)

    @mock.patch('spinnerchief.urllib2')
    def test_unique_variation_default_call(self, urllib2):
        """Test call of unique_variation() with default values."""
        # mock response from SpinnerChief
        mocked_response = base64.b64encode(u'This is my petž.'.encode("utf-8"))
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sc.unique_variation(u'This is my dogž.'),
            u'This is my petž.',
        )

    @mock.patch('spinnerchief.urllib2')
    def test_text_with_spintax_default_call(self, urllib2):
        """Test call of text_with_spintax_call() with default values."""
        # mock response from SpinnerChief
        mocked_response = base64.b64encode(
            u'This is my {dog|pet|animal}ž.'.encode("utf-8")
        )
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sc.text_with_spintax(u'This is my dogž.'),
            u'This is my {dog|pet|animal}ž.',
        )
