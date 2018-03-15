###################
phenodata changelog
###################

development
===========

2018-03-15 0.6.4
================
- Fix accidental version bump of the "docopt" module,
  see also https://github.com/peritus/bumpversion/issues/168
- Update documentation

2018-03-14 0.6.3
================
- Yet another documentation update

2018-03-14 0.6.2
================
- More documentation updates

2018-03-14 0.6.1
================
- Minor documentation updates

2018-03-14 0.6.0
================
- Add "--show-ids" parameter to show IDs alongside resolved text representation when using "--humanize"
- More compact date output for "tabular" mode
- Fix datetime coercion when encountering invalid datetime values
- Humanize searching in "observation" and "forecast" data for stations, species, phases and quality information
- Implement predefined sets of parameters using ``presets.json``.
  Apply with e.g. "--species-preset=mellifera-de-primary".
  See also https://community.hiveeyes.org/t/phanologischer-kalender-entwicklung/664/23.
- Reduce logging verbosity. Add progress bar for data acquisition step.
- Use "appdirs" module for computing cache storage location

2018-03-14 0.5.0
================
- Add commands "phenodata nearest-station" and "phenodata nearest-stations"
- Add parameter "--humanize" to improve user output by resolving ID columns
  to appropriate text representions from metadata files
- Update "Usage" section in README
- Add humanized representation for "forecast" mode
- Add "--sort" parameter for sorting by result columns
- Use shorter representation of humanized "Station" name

2018-03-14 0.4.0
================
- Refactoring and modularization
- Make FTP client wrapper for DWD CDC server more universal
- Improve inline documentation
- Improve CSV import string data cleansing and integer type coercion
- Improve filtering mechanics
- Filter by quality-level and quality-byte
- Add forecasting feature

2018-03-13 0.3.0
================
- Add command "phenodata observations" for acquiring observation data
- Filter observations by file names, station ids and years
- Add command "phenodata list-quality-bytes" for DWD
- Add option "--format={tabulate,json,csv}" for specifying output format

2018-03-12 0.2.0
================
- Add command "phenodata list-quality-levels" for DWD
- Add generic FTP resource caching honoring file modification time to speed up subsequent invocations

2018-03-12 0.1.0
================
- Implement commands list-species, list-phases and list-stations for data source DWD
- Improve release process
- Update documentation

2018-03-11 0.0.0
================
- Initial project skeleton
- Add initial documentation
- Add code basics
