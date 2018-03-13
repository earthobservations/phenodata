# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import sys
import logging

def boot_logging(options=None):
    log_level = logging.INFO
    if options and options.get('--debug'):
        log_level = logging.DEBUG
    setup_logging(level=log_level)

def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

def normalize_options(options, list_items=None):
    normalized = {}
    list_items = list_items or []
    for key, value in options.items():

        # Sanitize key
        key = key.strip('--<>')

        # Decode list options
        if key in list_items:
            if value is None:
                value = []
            elif type(value) is str:
                value = read_list(value)

        normalized[key] = value

    return normalized

def to_list(obj):
    """Convert an object to a list if it is not already one"""
    # stolen from cornice.util
    if not isinstance(obj, (list, tuple)):
        obj = [obj, ]
    return obj

def read_list(data, separator=u','):
    if data is None:
        return []
    result = list(map(lambda x: x.strip(), data.split(separator)))
    if len(result) == 1 and not result[0]:
        result = []
    return result
