#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

def xml_escape(text: str) -> str:
    result = text

    result = result.replace('\'', "\\'")
    result = result.replace('"', '\\"')
    result = result.replace('&', '&amp;')
    result = result.replace('<', '&lt;')
    result = result.replace('>', '&gt;')
    result = result.replace('@', '\\@')
    result = result.replace('?', '\\?')

    return result
