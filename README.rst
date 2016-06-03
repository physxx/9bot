9Bot
=======

.. image:: https://readthedocs.org/projects/votebot/badge/?version=latest
   :alt: Documentation status
   :target: http://votebot.readthedocs.io/en/latest/

.. image:: https://travis-ci.org/HE-Arc/votebot.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/HE-Arc/votebot

The bot for voting on stuff.

Installation
------------

This bot uses extensively features from Python 3.4.

.. code-block:: shell

    $ python -m venv slack
    $ cd slack
    $ . bin/activate
    (slack)$ pip install git+https://github.com/physxx/9bot


Usage
-----

.. code-block:: shell

    (slack)$ export SLACK_TOKEN=xoxb-123
    (slack)$ python 9bot
