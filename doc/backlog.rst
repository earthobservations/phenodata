#######
Backlog
#######


********
By topic
********

Bugs
====
- [o] Improve input data validation. Currently, the program croaks when

  - using ``--species-preset`` w/o ``--humanize``. Maybe implicitly select it?
  - acquiring "forecast" data with "--humanize" and "--show-ids" options
    https://github.com/earthobservations/phenodata/issues/6

Documentation
=============
- [o] Add remark about outdated ``--year`` values in README
- [o] Citation does not include description text

Code & refactoring
==================
- [o] Type annotations
- [o] Code formatting
- [o] Why are the ``dataset`` and ``partition`` options on different levels of the API?
- [o] Introduce Enum constants for annual vs. immediate, and recent vs. historical

Features
========
- [o] Produce condensed example like outlined within README » Output example
  => The ``forecast`` examples do that.
- [o] How long is data being cached?
- [o] Get rid of ``sql`` extra?
- [o] Look into acquiring data from the CDC portal instead of using the FTP/HTTP server

Infrastructure
==============
- [o] Provide Docker images
- [o] Migrate to ``pyproject.toml``, with all the bells and whistles like ``poe check``

Ideas
=====
- [o] Work on proposal for PPODB-next, see :ref:`ppodb`
- [o] Add HTTP API endpoint based on SQL interface
- [o] Add adapter for xpublish


**********
Unsorted I
**********
- [o] Switch from FTP to HTTP
- [o] What's a ``.zenodo.json`` file?
  https://github.com/citation-file-format/citation-file-format/blob/main/.zenodo.json
- [o] Why do some of the tests fail on CI/GHA/Linux?
- [o] Specify output order of columns


***********
Unsorted II
***********
- [o] Render like https://www.zamg.ac.at/zamgWeb/pict/phaenospiegel/archive/pheno_overview_Austria_web_1_2016.png
- [o] Display effective criteria just before performing the work
- [o] Output "phenodata info" as DataFrame
- [o] Complete offline mode running from - even stale - cache entries
- [o] Display progress indicator when downloading large files
- [o] What about introducing the BBCH code? ``--phase-bbch=60``
- [o] Revisit the "historical" data sets
- [o] Visualization: Exporter for vis.js timeline and Grafana annotations

  - https://community.hiveeyes.org/t/phanologischer-kalender-fur-trachtpflanzen/664/17
  - https://github.com/visjs/awesome-visjs
  - https://github.com/javdome/timeline-arrows
  - https://community.hiveeyes.org/t/phenodata-ein-datenbezug-und-manipulations-toolkit-fur-open-access-phanologiedaten/2892/25
- [o] See what Nominatim could do
- [o] Query directly by lat/lon instead of --station=
- [o] Enrich "Output example" in README.rst
- [o] Add --format=table-markdown, expanding to --format=tabular:pipe
- [o] For "--partition=historical", the file sizes are considerably larger. Think about displaying a per-file progress bar.
- [o] Don't skip "Kulturpflanze_Ruebe_akt" and "Kulturpflanze_Ruebe_hist"
- [o] Scan https://community.hiveeyes.org/t/phanologischer-kalender/664 for more bug reports and feature requests
- [o] Exporter for Kotori annotations, see https://community.hiveeyes.org/t/annotationen-im-grafana-uber-die-http-mqtt-api/111/17
- [o] Remark: Take care about filtering by "filename" vs. "species"
- [o] Adapter for ``mqtt-publish``
- [o] Adapter for exporting data into databases


*****
Notes
*****
- https://www.researchgate.net/publication/266211199_Guidelines_for_Plant_Phenological_Observations


****
Done
****
- [x] Introduce parameter "--format", which can be "tabulate:psql", "json", "xml", "vcf"
- [x] There are still spaces around, e.g. "phenodata list-phases --source=dwd --format=csv"
- [x] Filter by quality indicators
- [x] Add forecasting feature. Based on "Jultag"?
- [x] Add command "phenodata nearest-station --latitude= --longitude="
- [x] Improve flux compensator by joining observation data frames against metadata frames
- [x] Add parameter "--humanize" and "--language={german,english}
- [x] Parameter "shortstation"
- [x] Can the fine "tabulate" module can be tweaked to use custom datetime formatting (w/o the time component)?
- [x] Implement text-searching in stations, species, phases and quality information
- [x] Implement wishlist re. preselected groups of species as "mellifera" flavours
- [x] Suppress or move resource acquisition log messages to DEBUG log level and replace by progress indicator
- [x] Use "appdirs" module for computing cache storage location
- [x] Add command "phenodata drop-cache"
- [x] "Jultag" auch bei "--humanize" nicht unterdrücken wegen https://community.hiveeyes.org/t/phanologischer-kalender/664/45
- [x] ``appdirs`` => ``platformdirs``
- [x] Add ``CITATION.cff``
- [x] Docs: Library use
- [x] Test examples
- [x] Deprecation warnings re. pandas
- [x] Rework Usage » General section
- [x] Better hide the "forecasting" feature from GA
- [x] tqdm + logger improvements
- [x] Add section outlining SQL filtering
- [x] Alias --format:

  - tabular:pipe => markdown, md
  - tabular:rst => restructuredtext, rst
