#######
Backlog
#######


********
By topic
********

Bugs
====
- [o] Croaks when acquiring "forecast" data with "--humanize" and "--show-ids" options
  https://github.com/earthobservations/phenodata/issues/6

Features
========
- [o] Switch from FTP to HTTP
- [o] Docs: Add remark about outdated ``--year`` values in README
- [o] Get rid of ``sql`` extra?
- [x] Deprecation warnings re. pandas

Infrastructure
==============
- [o] Provide Docker images
- [o] Migrate to ``pyproject.toml``, with all the bells
  and whistles like ``poe check``


********
Unsorted
********
- [o] Render like https://www.zamg.ac.at/zamgWeb/pict/phaenospiegel/archive/pheno_overview_Austria_web_1_2016.png
- [o] Display effective criteria just before performing the work
- [o] Output "phenodata info" as DataFrame
- [o] Complete offline mode running from - even stale - cache entries
- [o] Display progress indicator when downloading large files
- [o] What about introducing the BBCH code? ``--phase-bbch=60``
- [o] Revisit the "historical" data sets
- [o] Exporter for vis.js timeline
- [o] See what Nominatim could do
- [o] Query directly by lat/lon instead of --station=
- [o] Enrich "Output example" in README.rst
- [o] Add --format=table-markdown, expanding to --format=tabular:pipe
- [o] For "--partition=historical", the file sizes are considerably larger. Think about displaying a per-file progress bar.
- [o] Don't skip "Kulturpflanze_Ruebe_akt" and "Kulturpflanze_Ruebe_hist"
- [o] Scan https://community.hiveeyes.org/t/phanologischer-kalender/664 for more bug reports and feature requests
- [o] Exporter for Kotori annotations, see https://community.hiveeyes.org/t/annotationen-im-grafana-uber-die-http-mqtt-api/111/17
- [o] Remark: Take care about filtering by "filename" vs. "species"
- [o] mqtt-publish adapter


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
