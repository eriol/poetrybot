poetrybot
=========

poetrybot is a Telegram bot to quote poems between friends. It's written in
Python and it is released under the EUPL 1.2 license.

Friends are defined by an allow list in which every account have to be in order
to to use the bot.
The management of the bot is provided by a REST API defined in the subpackage
``poetrybot.web``.


Installation
------------

1. Create your bot using Telegram `@BotFather <https://t.me/botfather>`_.
2. Install (preferably inside a virtualenv) the bot using:

   .. code-block::

      pip install poetrybot

3. The bot uses environment variables as configuration, you have to export the
   following before starting it:

   .. code-block::

      export AUTH_TOKEN=<my secret auth token>
      export DATABASE_URL=sqlite:////absolute/path/to/poetrybot.db
      export TELEGRAM_TOKEN=<telegram bot API key>

   ``AUTH_TOKEN`` is used to authenticate to the REST API used to manage the
   bot. Full specification is in the ``docs/openapi.yml`` file.
   Just create a long enough random string, for example using ``pwgen -sy 50``.
4. Launch the bot:

   .. code-block::

      poetrybot
5. To use the REST API install a WSGI HTTP Server, for example gunicorn, and
   then:

   .. code-block::

      gunicorn poetrybot.web.wsgi:app

6. Use the REST API to insert allowed friends, poets and poems. The fastest way
   to look at the API is to load the API specification into
   https://editor.swagger.io

An alternative is to clone the repository and use the provided ``Dockerfile``.

Usage
-----

To use the bot you only have to use the ``/quote`` command. The bot can be
added to one or more channels but it's not required. But remember that only
friends in allow list will be able to interact with the bot.

The ``/quote`` command used without parameters will make the bot to quote a
random poem, but optionally the author and the argument can be specified:

* ``/quote`` returns a random poem;
* ``/quote AUTHOR`` returns a random poem by ``AUTHOR``.

  ``AUTHOR`` is the name or part of the name of the poet case insensitive:

  .. code-block::

     /quote Giovanni Pascoli
     /quote pascoli
     /quote ascol

  will return a random poem by Giovanni Pascoli, if you don't have another
  poet with *ascol* inside the name;
* ``/quote AUTHOR about ARGUMENT`` returns a random poem by ``AUTHOR`` about
  ``ARGUMENT``.

  ``ARGUMENT`` is, like ``AUTHOR``, case insensitive and can be part of a word.
  ``about`` is, instead, case sensitive;
* ``/quote about ARGUMENT`` returns a random poem about ``ARGUMENT``.
