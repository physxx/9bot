9Bot
=======

Slack signifie "relâché" alors relâchez-vous (mais pas trop) et prenez une pause avec 9Bot ! 9Bot a pour but de faire profiter de 9gag sans souffrir de la folie du scroll.

9Bot est un bot pour Slack. Le but de 9Bot est d'envoyer à l'utilisateur des postes du site www.9gag.com lorsque celui-ci le demande.

Il est possible de demander des postes de la plupart des sections de 9gag. L'utilisateur peut également préciser le nombre de postes souhaités.

Voici la syntaxe de la commande : [section] [n]

section : Représente une section de 9gag. Exemples : hot, fresh, food...

n : Indique le nombre de postes désirés. Si n n'est pas précisé il vaudra 1.

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
    (slack)$ python slack9bot
