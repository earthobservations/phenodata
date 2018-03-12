.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/pypi/v/phenodata.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/github/tag/hiveeyes/phenodata.svg
    :target: https://github.com/hiveeyes/phenodata

|

#################################################
phenodata - phenology data acquisition for humans
#################################################


*****
About
*****
phenodata is a data acquisition and manipulation toolkit for open access phenology data.
It is written in Python.

Currently, it implements data wrappers for acquiring phenology observation data published
on the DWD Climate Data Center (CDC) FTP server operated by »Deutscher Wetterdienst« (DWD).

Under the hood, it uses the fine Pandas_ data analysis library for data mangling, amongst others.

.. _Pandas: https://pandas.pydata.org/


***************
Acknowledgments
***************
Thanks to the many observers, »Deutscher Wetterdienst«,
the »Global Phenological Monitoring programme« and all people working behind
the scenes for their commitment in recording the observations and for making
the excellent datasets available to the community. You know who you are.


***************
Getting started
***************

Install
=======
If you know your way around Python, installing this software is really easy::

    pip install phenodata --upgrade

Please refer to the `virtualenv`_ page about further recommendations how to install and use this software.

.. _virtualenv: https://github.com/hiveeyes/phenodata/blob/master/doc/virtualenv.rst


Usage
=====
Display list of species::

    phenodata list-species --source=dwd

Display list of phases::

    phenodata list-phases --source=dwd

Display list of stations::

    phenodata list-stations --source=dwd --dataset=immediate


Proposal
========
Display regular flowering events for hazel and snowdrop around Berlin and Brandenburg (Germany) in 2017::

    phenodata tabular --source=dwd --dataset=immediate --year=2017 --regions=berlin,brandenburg --species=hazel,snowdrop --phase=flowering

Display forecast for "beginning of flowering" events for canola and sweet cherry around Thüringen and Bayern (Germany)::

    phenodata tabular --source=dwd --dataset=immediate --forecast --regions=thüringen,bayern --species=raps,süßkirsche --phase-bbch=60

.. warning:: These commands are not implemented yet.

You can choose between two different datasets, `annual-reporters`_ and `immediate-reporters`_.

.. _annual-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/jahresmelder/jahresmelder_node.html
.. _immediate-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/sofortmelder/sofortmelder_node.html


*******************
Project information
*******************

About
=====
The "phenodata" program is released under the AGPL license.
The code lives on `GitHub <https://github.com/hiveeyes/phenodata>`_ and
the Python package is published to `PyPI <https://pypi.org/project/phenodata/>`_.
You might also want to have a look at the `documentation <https://hiveeyes.org/docs/phenodata/>`_.

The software has been tested on Python 2.7.

If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Code license
============
Licensed under the AGPL license. See LICENSE file for details.

Data license
============
The DWD has information about their re-use policy in German and English.
Please refer to the respective Disclaimer
(`de <https://www.dwd.de/DE/service/disclaimer/disclaimer_node.html>`_,
`en <https://www.dwd.de/EN/service/disclaimer/disclaimer.html>`_)
and Copyright
(`de <https://www.dwd.de/DE/service/copyright/copyright_node.html>`_,
`en <https://www.dwd.de/EN/service/copyright/copyright_artikel.html>`_)
information.

Disclaimer
==========
The project and its authors are not affiliated with DWD, USA-NPN or any
other data provider in any way. It is a sole project from the community
for making data more accessible in the spirit of open data.
