###################
phenodata changelog
###################

development
===========

2023-04-11 0.12.0
=================
- Fix ``nearest-station`` with ``--format=json``
- Fix filtering by ``int64``-type identifiers, see GH-7
- Fix SQL filtering with DuckDB
- Tests: Add software tests
- Improve documentation
- CI: Add GHA configuration to invoke software tests
- CI/Tests: Fix installation on Python 3.7 to 3.9
- Dependencies: Switch from ``appdirs`` to ``platformdirs``
- Dependencies: Add compatibility with pandas 2
- Docs: Add `examples` snippets to README and tests
- Tests: Add code snippet in README to test suite, per doctest
- Docs: Add configuration for "Read the Docs"
- Docs: Make the "forecast" feature less prominent, because it
  only offers a naive approach.
- Docs: Add proselint

2020-12-29 0.11.0
=================
- Add ``--sql`` option to postprocess the egress dataframe using SQL

2020-12-29 0.10.0
=================
- Add ``--forecast-year`` option

2020-12-29 0.9.4
================
- Be more graceful if some filter constraints are not given

2020-12-28 0.9.3
================
- Update wrong link to PyPI download count badge
- Fix virtualenv options

2020-12-28 0.9.2
================
- Add basic examples about how to use the module as a library
- Relax dependencies to be able to use a more recent version of Pandas
- Be graceful about malformed lines within ingress CSV
- Work around deprecated Pandas feature regarding index vs. column ambiguity

2020-01-07 0.9.1
================
- Update version badge within README header

2020-01-07 0.9.0
================
- Upgrade release support packages "twine" and "keyring"
- Change base URL to new opendata URL. Thanks, @mgrrx.
- Futurize for Python 3 compatibility.

2018-03-29 0.8.0
================
- Add option "--sort=" to "phenodata list-stations" for filtering by arbitrary text strings

2018-03-29 0.7.0
================
- Don't display multi-index column in "forecast" mode w/o "humanize" option
- Grok species "Rübe" by applying appropriate fixups to raw data before parsing
- Add option "--filter=" to "phenodata list-stations" for filtering by arbitrary text strings

2018-03-28 0.6.5
================
- Add some sanity checks protecting against empty intermediate results
- Add "--verbose" option for enabling the DEBUG log level in turn displaying processed files
- Also skip file "Kulturpflanze_Ruebe_hist" completely as it has an invalid header format (all caps)
- Also skip files matching "PH_.+_Notiz" completely as they contain metadata
- Improve empty value removal before postprocessing
- Add column "Tag" for "--humanize" option

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
- Make FTP client wrapper for DWD CDC server universal
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
