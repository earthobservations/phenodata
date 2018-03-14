# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import os
import re
import arrow
import shutil
import appdirs
import logging
import requests_ftp
import dogpile.cache
from phenodata.util import regex_make_matchers, regex_run_matchers

logger = logging.getLogger(__name__)

class CacheManager(object):

    def __init__(self):

        # Path to cache directory, system agnostic
        self.cache_path = os.path.join(appdirs.user_cache_dir(appname='phenodata', appauthor=False), 'dwd-ftp')
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        # Setup cache regions
        self.setup()

    def setup(self):

        logger.info('The cache directory is {}'.format(self.cache_path))

        # Generic metadata cache with an expiration time of 5 minutes
        # See also ``listplus``.
        self.meta = dogpile.cache.make_region().configure(
            "dogpile.cache.dbm",
            expiration_time=60 * 5,
            arguments={
                "filename": os.path.join(self.cache_path, 'meta-cache.dbm'),
            }
        )

        # Content cache using a custom mechanism honoring modification time
        # on server (mtime). See also ``retr_cached``.
        self.content = dogpile.cache.make_region().configure(
            "dogpile.cache.dbm",
            arguments={
                "filename": os.path.join(self.cache_path, 'content-cache.dbm'),
            }
        )

    def drop(self):
        logger.info('Dropping cache at {}'.format(self.cache_path))
        shutil.rmtree(self.cache_path)
        return True


class FTPSession(requests_ftp.ftp.FTPSession):
    """
    An improved version of the `requests-ftp`_ module featuring a few additional methods:

    - ``mtime``:        Get modification time of file on server
    - ``list_plus``:    Get directory contents in a structured manner, with short-time response caching
    - ``scan_files``:   Scan three-level hierarchy of directories on FTP server, can apply filters
    - ``retr_cached``:  Get file contents, with response caching using mtime-based expiry

    Furthermore, the module applies response caching mechanisms for each interaction with the
    remote FTP server to speed up subsequent invocations. There are two different cache regions:

    - meta:             A generic FTP metadata cache with a configurable expiration time (currently 5 minutes)
    - content:          A generic FTP resource cache honoring file modification time

    .. _requests-ftp: https://pypi.python.org/pypi/requests-ftp
    """

    def ensure_cache_manager(self):
        if not hasattr(self, 'cache'):
            self.cache = CacheManager()

    def mtime(self, url):
        """
        Get modification time of file on server.

        Uses the ``list_plus`` method, so it isn't a performance hog
        by offering short-time caching of FTP server responses.
        """

        # Read contents of container directory
        directory = os.path.dirname(url)
        entries = self.list_plus(directory)

        # Build dictionary mapping file url to its modification time for easier lookup
        name_mtime_map = {}
        for entry in entries:
            name_mtime_map[entry['url']] = entry['mtime']

        # Resolve modification time of designated file url
        mtime = name_mtime_map.get(url)

        return mtime

    def list_plus(self, url):
        self.ensure_cache_manager()
        key = 'list:{}'.format(url)
        return self.cache.meta.get_or_create(key, lambda: self.list_plus_real(url))

    def list_plus_real(self, url):
        """
        Get directory contents in a structured manner, with short-time response caching.
        It offers short-time caching of FTP server responses to speed up subsequent invocations.
        """

        logger.info('Send FTP LIST command for {}'.format(url))

        # Send FTP LIST command
        response = self.list(url)
        #print 'FTP list response:\n{}'.format(response.content)
        if response.status_code != 226:
            message = 'FTP LIST command for {} failed'.format(url)
            logger.warning(message)
            return []

        # Decode LIST response
        entries = []
        for line in response.content.split('\n'):

            # Skip empty lines
            line = line.strip()
            if not line: continue

            # Decode line format
            parts = re.split('\s+', line)
            size = int(parts[4])
            mtime = ' '.join(parts[5:8])
            filename = parts[8]

            # Parse modification date
            # https://arrow.readthedocs.io/en/latest/#arrow.factory.ArrowFactory.get
            # https://arrow.readthedocs.io/en/latest/#tokens
            # Examples: Mar 2 04:09, Jun 1 2017
            mtime = arrow.get(mtime, ['MMM D HH:mm', 'MMM D YYYY'])
            if mtime.year == 1:
                # FIXME: Use current year instead of 2018
                mtime = mtime.replace(year=2018)

            # Build directory entry
            entry = {
                'size': size,
                'mtime': mtime,
                'name': filename,
                'url': os.path.join(url, filename)
            }
            entries.append(entry)

        return entries

    def scan_files(self, url, subdir=None, include=None, exclude=None, include_base=None, exclude_base=None):
        """
        Scan three-level hierarchy of directories on FTP server.
        Applies include and exclude filters appropriately
        while iterating directory contents.
        """

        # Bundle filter patterns
        filter = {
            'include': include,
            'exclude': exclude,
            'include_base': include_base,
            'exclude_base': exclude_base,
        }

        # Regex-compile filter patterns, inplace
        for key, value in filter.items():
            value = value or []
            value = regex_make_matchers(value)
            filter[key] = value

        # Read directory contents from FTP server
        child_items = self.list_plus(url)

        # Names of direct child directories
        child_names = [entry['name'] for entry in child_items]

        # Compute list of designated results
        results = []

        # Iterate direct child directories
        for child_name in child_names:

            # Compute full URL to resource, optionally adding
            # yet another "subdir" level obtained as method parameter.
            path = [url, child_name]
            if subdir:
                path.append(subdir)

            # Read directory contents of data directory
            data_directory = '/'.join(path)
            data_files = self.list_plus(data_directory)

            # Iterate files in data directory
            for entry in data_files:

                # Apply a bunch of include/exclude filters
                filename = entry['name']

                if filter['include_base']:
                    if not regex_run_matchers(filter['include_base'], filename):
                        continue

                if filter['exclude_base']:
                    if regex_run_matchers(filter['exclude_base'], filename):
                        continue
                if filter['exclude']:
                    if regex_run_matchers(filter['exclude'], filename):
                        continue

                if filter['include']:
                    if not regex_run_matchers(filter['include'], filename):
                        continue

                # Use this entry as it satisfied all filters
                results.append(entry)

        return results

    def retr_cached(self, url, strip_base=None):
        """
        Get file contents, with response caching.

        The caching mechanism honors the modification time (mtime)
        of the addressed resource on the remote FTP server,
        so its cache slot will be updated appropriately.

        Obtains parameter ``strip_base`` to strip prefix string
        from full URLs for using them in log messages.
        """

        self.ensure_cache_manager()

        # Prepare short URL for logging
        shorturl = url
        if strip_base:
            shorturl = url.replace(strip_base, '')

        # Request modification time of resource
        mtime = self.mtime(url)
        logger.debug('Resource "{resource}": Last modified on "{mtime}"'.format(resource=shorturl, mtime=mtime))

        # Default payload: Empty
        payload = None

        # Compute cache keys
        content_key = 'content:{resource}'.format(resource=url)
        mtime_key = 'mtime:{resource}'.format(resource=url)

        # Retrieve modification time of cached item
        mtime_cached = self.cache.content.get(mtime_key)

        # Get item from cache if not expired
        if mtime_cached and mtime <= mtime_cached:
            logger.debug('Resource "{resource}": Loading from cache'.format(resource=shorturl))
            payload = self.cache.content.get(content_key)

        # Retrieve resource from FTP if it is stale or has not been cached yet
        if payload is None:

            # Retrieve resource from upstream
            logger.debug('Resource "{resource}": Retrieving from FTP'.format(resource=shorturl))
            response = self.retr(url)

            # Populate cache with valid response content
            if response.status_code == 226:
                payload = response.content
                self.cache.content.set(content_key, payload)
                self.cache.content.set(mtime_key, mtime)

            # Handle resource missing
            elif response.status_code == 404:
                message = 'Resource "{}" does not exist ({})'.format(url, response.status_code)
                logger.warning(message)

            # Handle failed responses
            else:
                message = 'Resource "{}" failed ({})'.format(url, response.status_code)
                logger.warning(message)

        return payload
