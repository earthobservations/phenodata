# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import re
import sys
import math
import logging
import numpy as np


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

def normalize_options(options, encoding=None, list_items=None):
    normalized = {}
    for key, value in options.items():

        # Sanitize key
        key = key.strip('--<>')

        # Sanitize charset encoding
        if encoding and (type(value) is str):
            value = value.decode(encoding)

        normalized[key] = value

    return normalized

def options_convert_lists(options, list_items=None):
    list_items = list_items or []
    for key, value in options.items():
        # Decode list options
        if key in list_items:
            if value is None:
                value = []
            else:
                value = read_list(value)
            options[key] = value

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

def regex_make_matchers(patterns):
    matchers = []
    for pattern in to_list(patterns):
        pattern = '.*{}.*'.format(pattern)
        matchers.append(re.compile(pattern))
    return matchers

def regex_run_matchers(matchers, text):
    for matcher in matchers:
        if matcher.match(text):
            return True
    return False

def dataframe_strip_strings(col):
    # https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha/44740438#44740438
    if col.dtypes == object:
        return (col.astype(unicode)
                .str.strip(' \t')
                .replace({'nan': np.nan}))
    return col

def dataframe_coerce_columns(df, columns, datatype):
    # https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas/47303880#47303880
    # https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas/44536326#44536326
    df[columns] = df[columns].astype(datatype)

def haversine_distance(destination, origin):
    # Stolen from https://github.com/marians/dwd-weather
    lon1, lat1 = origin
    lon2, lat2 = destination
    radius = 6371000 # meters

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d
