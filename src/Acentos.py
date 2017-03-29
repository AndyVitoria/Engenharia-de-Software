#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')


