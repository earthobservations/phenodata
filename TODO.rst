##############
phenodata todo
##############

******
Prio 1
******
- [x] Introduce parameter "--format", which can be "tabulate:psql", "json", "xml", "vcf"
- [x] There are still spaces around, e.g. "phenodata list-phases --source=dwd --format=csv"
- [x] Filter by quality indicators
- [x] Add forecasting feature. Based on "Jultag"?
- [x] Add command "phenodata nearest-station --latitude= --longitude="
- [x] Improve flux compensator by joining observation data frames against metadata frames
- [x] Add parameter "--humanize" and "--language={german,english}
- [o] Implement text-searching in stations, species, phases and quality information
- [o] Implement wishlist re. preselected groups of species as "mellifera" flavours

******
Prio 2
******
- [o] Use "appdirs" module for improving cache storage location
- [o] Add command "phenodata purge-cache"
- [o] Output "phenodata info" as DataFrame
- [o] Complete offline mode running from - even stale - cache entries
- [o] Move resource acquisition log messages to DEBUG log level and replace by progress indicator
- [o] Display progress indicator when downloading large files
- [o] What about the BBCH code?
