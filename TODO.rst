##############
phenodata todo
##############

- [x] Introduce parameter "--format", which can be "tabulate:psql", "json", "xml", "vcf"
- [o] Add command "phenodata purge-cache"
- [o] Add command "phenodata nearest-station --latitude= --longitude="
- [o] Filter by quality indicators
- [o] There are still spaces around, e.g. "phenodata list-phases --source=dwd --format=csv"
- [o] Add parameter "--humanize" and "--lang={german,english}
- [o] Complete offline mode running from - even stale - cache entries
- [o] Move resource acquisition log messages to DEBUG log level and replace by progress indicator
- [o] Improve flux compensator by joining observation data frames against metadata frames
- [o] Use "appdirs" module for improving cache storage location
- [o] Output "phenodata" info as DataFrame
