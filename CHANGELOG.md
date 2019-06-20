# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Documentation at https://developer.blackfynn.io/python/


## [2.13.1]
### Changed
- Fixed wrong tag for release + documentation about release

## [2.13.0]
### Removed
- State of packages can no longer be set through this library 
- Non functional. DO NOT USE

## [2.12.0]
### Removed
- Separate host for Models API

## [2.11.1]
### Changed
- Using relate_to on concepts now populates the source and destination of the relationship

## [2.11.0]
### Changed
- Knowledge graph query results now include the records of models specified
  in a `join()`.

## [2.10.0]
### Changed
- Added query support to knowledge graph models.

## [2.9.2]
### Fixed
- Backwards-incompatible errors caused by old versions of the Agent. You now must explicitly pass `use_agent=True` to enable uploads via the Blackfynn CLI Agent.

## [2.9.1]
### Fixed
- Bugs in progress bars when using the Agent for uploads

## [2.9.0]
### Changed
- The `bf` Python CLI is deprecated and will be removed in a future release. Please install and use the new Blackfynn CLI Agent https://developer.blackfynn.io/agent.

### Added
- The Python client can now use the Blackfynn CLI Agent for large file uploads
- Newly created Blackfynn datasets no longer process all uploaded data. Pass `automatically_process_packages=True` to `create_dataset` to revert to the old behavior.
- Added `Dataset.get_connected_models` and `Model.get_connected` methods to retrieve topologically connected models.

## [2.8.0]
- Added `Dataset.status` for viewing the current status of a dataset
- Added `Dataset.get_graph_summary` method for retrieving high-level statistics about the graph

## [2.7.2]
### Changed
- Deprecated the following `Dataset` methods: `collaborators`, `add_collaborators`, and `remove_collaborators`. Permissions should now be managed through the Blackfynn web app.

## [2.7.1]
### Fixed
- Removed limit on the number of related records that can be retrieved

## [2.7.0]
### Changed
- Make ModelTemplate category param optional in constructor

## [2.6.6]
### Changed
- Added knowledge graph tutorial in documentation

## [2.6.5]
### Fixed
- Retrieval of all annotations for a timeseries

### Changed
- Added support for Python 3.7
- Refactored checks that channels belong to a given timeseries

## [2.6.4]
### Fixed
- Loading of non-enumerated array properties

## [2.6.3]
### Fixed
- Automatic releases via Travis (again)

## [2.6.2]
### Fixed
- Automatic releases via Travis

## [2.6.1]
### Changed
- Settings overridden via function arguments will be prioritized over settings overridden by environment variables
- Documentation updates
- Added descriptions to properties

### Fixed
- Divide-by-zero error during empty file upload

## [2.6.0]
### Added
- Support for Python 3!

### Changed
- The `upload()` methods of `Dataset` and `Collection` objects and the
  `append_files()` method of `TimeSeries` can now be passed a list of files or
  separate file arguments.
- Updated documentation and documentation URLs.
- Unpinned version of the `pytz` dependency.

### Fixed
- Fixed overrides of concept and streaming API hosts.

### Removed
- `TimeSeries` streaming upload API.
- Deprecated `set` and `append` methods.

## [2.5.0]
### Added
- Support for topology endpoints

### Changed
- Client now raises an exception when creating a dataset with an existing name
- Removed concurrent requests capabilities
- Improved timeout and retry handling

### Fixed
- `owner_id` property on datasets and packages
- Deadlock caused by importing the client from another module

### Removed
- Ledger API

## [2.4.6]
### Added
- Support for model templates
### Changed
- Cleaned up Travis config
- Updated to use new date format

## [2.4.5]
### Changed
- Added a new release target which will build images on each new release that can be used to run unit tests.
- Updated concepts instance delete function to handle new response

## [2.4.4]
### Changed
- Updated documentation

## [2.4.3]
### Changed
- Resolved issue related to timed out APIs calls during file upload

## [2.4.2]
### Added
- Channels can be deleted by `id`
- A `gap_factor` argument has been added to `segments` and `get_segments` timeseries functions
- Pull request templates

### Changed
- Standardized logging methodology (no more print statements)
- Creating a model with invalid properties will no longer fail - the model will be created without any properties and an error will be logged
- Fixed `delete_annotation_layer` and `delete_annotation`
- Updated `query_annotation_counts` in accordance with updates to the concepts service
- `RecordSet`.`as_dataframe` now accepts a `record_id_column_name` arg to optionally include the record_id in the dataframe

## [2.3.0]
### Added
- Preliminary graph features, beta-quality
- Basic timeseries segments functionality
- Documentation dump (needs revision)

### Changed
- Upload using preview/grouping endpoint

## [2.1.4]
### Added
- A field for `size` to the File model

### Changed
- Models after updates to package, dataset, user, and organization API endpoints

## [2.1.3]
### Changed
- Updated `_update_self` to more reliably rely on model IDs for self verification

## [2.1.1]
### Changed
- Fixed re-authentication by maintaining organization context

## [2.1.0]
### Added
- `bf.members` function to return the members of the current organization
- Separation of CLI only and client code

### Changed
- Better working_dataset handling
- Timeseries query format has changed for the rest endpoint. Previously returned two arrays - times and values. Now returns a single array of time,value pairs.

## [2.0.3]
### Changed
- Only create cache directory if using cache

### Added
- `bf.context.members` property to get list of current org's users

## [2.0.1]
### Changed
- Use psutil for cross-platform os process support

## [2.0.0]
### Changed
- Model after new package and datasets API endpoints

## [1.8.4]
### Added
- Environment variable support for `s3_host` and `s3_port` (used mostly internally)

### Changed
- Collection/Dataset `print_tree()` function to work with utf-8 encoded names
- Debug print on threaded upload errors.

## [1.8.1]
### Added
- Local caching
- Profile handling

### Changed
- API Tokening for login instead of username/password
- Command line interface restructuring

## [1.7.5] - 2017-07-27
### Added
- Printing path of datasets for CLI
- Appending annotation files in client (bf append, ts.append_annotation_file)
- Support upload of .bfannot alongside timeseries files
- Write annotations from timeseries package to .bfannot file (ts.write_annotations)

### Changed
- Fixes for operating on 32bit machines due to overflow from UTC timestamps

## [1.7.4] - 2017-07-14
### Added
- Bug fix for adding channel specific annotations
- Documentation additions

## [1.7.3] - 2017-07-06
### Removed
- Misc Bug Fixes

## [1.7.2] - 2017-06-29
### Added
- Optimization of uploads
- Enabled recursive upload of folders
- Enabled upload/append of annotations (.bfannot) to timeseries packages
- Ledgers

### Changed
- Reworked Annotations
    - add, insert layers and annotations functions updated
- Reduced thread count for parallel uploads

## [1.6.2] - 2017-06-01
### Added
- Initial commit
