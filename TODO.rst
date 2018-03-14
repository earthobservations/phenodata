##############
phenodata todo
##############

******
Prio 1
******
- [x] Introduce parameter "--format", which can be "tabulate:psql", "json", "xml", "vcf"
- [x] There are still spaces around, e.g. "phenodata list-phases --source=dwd --format=csv"
- [x] Filter by quality indicators
- [o] Add forecasting feature. Based on "Jultag"?
- [o] Add command "phenodata nearest-station --latitude= --longitude="
- [o] Add parameter "--humanize" and "--lang={german,english}
- [o] Improve flux compensator by joining observation data frames against metadata frames

******
Prio 2
******
- [o] Use "appdirs" module for improving cache storage location
- [o] Add command "phenodata purge-cache"
- [o] Output "phenodata info" as DataFrame
- [o] Complete offline mode running from - even stale - cache entries
- [o] Move resource acquisition log messages to DEBUG log level and replace by progress indicator
- [o] Display progress indicator when downloading large files
