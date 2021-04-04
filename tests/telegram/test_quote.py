"""Tests for the quote command."""

import pytest

from poetrybot.telegram.commands.quote import parse_quote


def test_parse_quote():

    author, argument = parse_quote("")
    assert author is None
    assert argument is None

    author, argument = parse_quote("/quote Giovanni Pascoli")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote  Giovanni Pascoli ")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote Giovanni Pascoli about")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote Giovanni Pascoli about cielo")
    assert author == "Giovanni Pascoli"
    assert argument == "cielo"

    author, argument = parse_quote("/quote about cielo")
    assert author is None
    assert argument == "cielo"

    author, argument = parse_quote("/quote@bot")
    assert author is None
    assert argument is None

    author, argument = parse_quote("/quote@bot Giovanni Pascoli")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote@bot  Giovanni Pascoli ")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote@bot Giovanni Pascoli about")
    assert author == "Giovanni Pascoli"
    assert argument is None

    author, argument = parse_quote("/quote@bot Giovanni Pascoli about cielo")
    assert author == "Giovanni Pascoli"
    assert argument == "cielo"

    author, argument = parse_quote("/quote@bot about cielo")
    assert author is None
    assert argument == "cielo"
