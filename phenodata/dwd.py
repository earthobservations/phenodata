# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import attr
import logging

logger = logging.getLogger(__name__)

@attr.s
class DwdDataAcquisition(object):

    dataset = attr.ib()

    def get_species(self):
        pass

    def get_phases(self):
        pass

    def get_stations(self):
        pass
