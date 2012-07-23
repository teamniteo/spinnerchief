====================================
Python bindings for SpinnerChief API.
====================================

`Spinner Chief <http://www.spinnerchief.com/>`_ is an online
service for spinning text (synonym substitution) that creates unique version(s)
of existing text. This package provides a way to easily interact with
`SpinnerChief API <http://developer.spinnerchief.com/API_Document.aspx>`_.
Usage requires an account, `get one here <http://account.spinnerchief.com/>`_
and an api key which you get by registering
a `developer account <http://developer.spinnerchief.com/>`_.

* `Source code @ GitHub <https://github.com/niteoweb/spinnerchief>`_


Install within virtualenv
=========================

.. code::

    $ virtualenv foo
    $ cd foo
    $ git clone https://github.com/niteoweb/spinnerchief
    $ bin/pip install spinnerchief/

    # running tests:
    $ bin/pip install unittest2 mock
    $ bin/python -m unittest discover -s spinnerchief/src/spinnerchief/tests


Buildout
========

    $ git clone https://github.com/niteoweb/spinnerchief
    $ cd spinnerchief
    $ wget http://svn.zope.org/*checkout*/zc.buildout/branches/2/bootstrap/bootstrap.py
    $ python bootstrap.py
    $ bin/buildout

    # running tests:
    $ bin/py -m unittest discover -s src/spinnerchief/tests

    # check code for imperfections
    $ bin/vvv src/spinnerchief


Usage
=====

    >>> import spinnerchief
    >>> sc = spinnerchief.SpinnerChief("<yourapikey>", "<yourusername>", "<yourpassword>")

    >>> print sc.text_with_spintax(text="My name is Ovca!")
    {I am|I'm|My friends call me|Throughout southern california|Im} Ovca!

    >>> print sc.unique_variation(text="My name is Ovca!")
    Throughout southern california Ovca!

    >>> print "used: %s" % sc.quota_used()
    used: 2

    >>> print "left: %s" % sc.quota_left()
    left: 18
