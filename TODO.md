# Double Stars TODO List

## Version 0.1 - Pre-Release

- [X] Add argparse handling of input files and columns, outputs
- [X] Get default license headers ready and in place
- [X] Add license headers to double star code
- [X] Finish output of modified table in HTML and fits
- [X] Add SAO number to parsing
- [ ] Create main github project
- [X] Create README.md
- [X] Write README.md section on getting your own list working
- [X] Fix default formatting of table columns
- [X] Fix coordinate formatting issues (SimbadIdent & astroquery)
- [X] Make SimbadIdent consistent with astroquery
- [X] Refactor out SimbadIdent
- [X] Implement SimbadStarQuery class and get it working
- [X] Better handling of corner cases, e.g. "psi Psc"
- [X] Check it works on other examples, get correct names for other examples
- [X] Move general utilities into separate file
- [X] Fix remaining issues with whitespace and \n in star names
- [X] Have SimbadStarQuery store and output original user's ID.
- [X] Have input/output column names, hardwired for now.
- [X] Make star name aliases user-configurable and input to SimbadStarQuery
- [X] Add alternate txt file input possible, add input file type detection
- [X] Fix identifier handling for two-word star names, e.g Barnard's Star
- [X] Check input column name handling works, handles errors well
- [X] Add Fe_H Teff columns as its available

## Future Versions

- [ ] Script to download WDS data table directly from CDS.
- [ ] Python script to edit "bad" fits header keywords, e.g. in WDS.
- [ ] Python script to process output of star_query.py to get clean WDS IDs
- [ ] Python script to parse WDS data to get multiples.
- [ ] Clean up existing python related to Prieto et al data.
- [ ] Have configurable input/output column names, formats, descriptions
- [ ] Make votable fields used configurable as part of input/output column name config
- [ ] Better PEP8 compliance
- [ ] Full docstring and/or Sphinx documentation
- [ ] Unit tests!
- [ ] Possibly handle multiple distinct inputs, e.g. '42-45 Ori'
