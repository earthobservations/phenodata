###################
phenodata changelog
###################

development
===========

2018-03-13 0.3.0
================
- Add command "phenodata observations" for acquiring observation data
- Filter observations by file names, station ids and years
- Add command "phenodata list-quality-bytes"
- Add option "--format={tabulate,json,csv}" for specifying output format

2018-03-12 0.2.0
================
- Add command "list-quality-levels" for DWD
- Add generic FTP resource caching honoring file modification time to speed up subsequent invocations

2018-03-12 0.1.0
================
- Implement list-species, list-phases and list-stations for data source DWD
- Improve release process
- Update documentation

2018-03-11 0.0.0
================
- Initial project skeleton
- Add initial documentation
- Add code basics
