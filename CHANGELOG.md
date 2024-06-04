# Changelog
All notable changes to this project will be documented in this file.

# 1.3.4 - 2024-06-04
- Updated [dao_analyzer_components](./dao_analyzer_components/README.md) dependencies
- Updated dao-scripts to 1.5.0

# 1.3.3 - 2024-06-03
- Updated dao-scripts to 1.4.6
- Changed some network names
- Updated dependencies

# 1.3.1 - 2024-05-27
- Updated dao-scripts to 1.3.1

# 1.3.0 - 2024-05-27
- Updated dao-scripts to 1.3.0, now The Graph API key is needed to download data
- Updated dependencies
- Added Python 3.12 support

# 1.2.7 - 2023-09-05
- Moved cache-scripts to its own package ([dao-scripts](https://pypi.org/project/dao-scripts/))
- Updated dependencies

# 1.2.6 - 2023-05-11
- Small style fixes and typos
- [Updated cache-scripts](./cache_scripts/CHANGELOG.md) to 1.1.9

# 1.2.5 - 2023-02-24
- Updated README and ABOUT to add Zenodo and Kaggle
- Created script to deploy data to Zenodo and Kaggle

# 1.2.4 - 2023-02-20
- Updated README and ABOUT to add CSCW's demo
- [Updated cache-scripts](./cache_scripts/CHANGELOG.md)
- Fixed small typo on Aragon's votes graph title

# 1.2.3 - 2022-10-08
- Fixed [#118](https://github.com/Grasia/dao-analyzer/issues/118)

# 1.2.2 - 2022-10-03
- Fixed [#117](https://github.com/Grasia/dao-analyzer/issues/117)

# 1.2.1 - 2022-09-30
- Improved network selector
- Added the DAOA_DW_PATH env variable
- Fixed problems with DataPoint component when value was 0

# 1.2.0 - 2022-09-27
- System of Dash Components (faster loading time)
- Fixed error with Dropdown
- Improved installation and setup
- Added cli options to daoa-server
- Minor visual improvements

# 1.1.2 - 2022-08-09
- Fixing [#100](https://github.com/Grasia/dao-analyzer/issues/100)
- Added logging rotations

## 1.1.1 - 2022-07-27
- Fixed CSS bug

## 1.1.0 - 2022-07-20
- Added filter dropdown by DAO activity
- Added filter DAOs by Network
- Added DAOstack creation date
- Added URL search params
- Bugs removed

## 1.0.1 - 2022-06-10
- Added Equality Stats to Aragon
- Fixed participation stats when less than 1%

## 1.0.0 - 2022-06-07
**The CSCW update**
- Added timezone to last_update
- Updated some things in cache_scripts
  - Made all collectors updatable
- Created install scripts and published to pypi
- Added ABOUT page
- Added more Aragon Names
- Changed activity plots to calendar plots
- Using organizations store (faster response time)
- Added filtering (DAOs active last year)
- Added participation equality stats
- Added CITATION.cff
- Added total members graph to Aragon DAOs
- Changed frontend
  - Now using bootstrap
  - Changed header (logo and keyphrase)
  - Changed favicon
  - Added number of DAOs below the dropdown menu
  - Added disclaimers to some charts
  - Removed charts subtitles
  - Added platform and dao info
  - Added card with dao/platform datapoints
  - Changed last update location
  - Added current version to footer
  - Changed images to bootstrap icons

## 0.8.2 - 2022-03-30
- Changed last_update
- Fixed Docker workflow
- Display sections using tabs

## 0.8.1 - 2022-03-28
- Showing timezone in last update
- Solved pandas warnings
- Fixed init.sh
- Using last_update instead of block information

## 0.8.0 - 2022-03-24
- Obtaining holdings of DAOs (ERC-20 tokens)
- Displaying assets of DAOs
  - Assets with values using treemap
  - Assets with unknown value using a table
- Mobile view optimizations
- Making DAO address smaller ([#53](https://github.com/Grasia/dao-analyzer/issues/58))
- Showing last update time
- Fixed [#58](https://github.com/Grasia/dao-analyzer/issues/58)
- Fixed [#61](https://github.com/Grasia/dao-analyzer/issues/61)
- Added JoinCacheRequester

## 0.7.2 - 2022-03-01
- Added version number to footer

## 0.7.1 - 2022-02-07
- Supporting Python 3.10
- Removed deprecated things
- Refactored (vectorized) some Pandas code
- Added Matomo Analytics support
- Made some more collectors updatable
- Fixed some tests
- Fixed some newly updatable cache_scripts
- Made data updatable while running
  - Added advisory file locking to datawarehouse
  - CacheRequester respects the datawarehouse file lock, and keeps the data in memory if possible
  - cache_scripts are run on a temp folder without disturbing the datawarehouse

## 0.7.0 - 2021-11-30
The `cache_scripts` backend update
- Half the lines of code, a lot of new capabilities
- FIXED an important bug which caused some items to not be requested. Now every request is made to the same block.
- Fixed some important bugs
- Improved some requests so they take less time
- Added update mode so subsequent requests take less time (enabled by default)
- Changed .csv format of the datawarehouse to .arr (apache's feather)
- Displaying progress bars usign tqdm, and other progress methods
- Added caching to DAOHaus DAO Names
- Modified metadata format, now includes last update and blocks
- Added CLI option to select which collectors to run
- Added CLI option to select the date of the block to request
- Added CLI option to select where to download the data
- Logging to file inside datawarehouse

## 0.6.1 - 2021-11-02
Continuation of the `cache_scripts` interface update
- Added method of selecting which networks to update on CLI
- Added aragon names retrieval (from Aragon Client's code)
- Added url sharing capabilities (each DAO now has a different URL)
- FIXED problem with data retrieval (was only retrieving first 5k items)

## 0.6.0 - 2021-10-15
The `cache_scripts` update!

- Added CLI to cache_scripts
  - You can choose which platforms to update
  - You can select if you want to stop on errors
  - Added progress bar for long processes
- Added logger to cache_scripts
- Added support for more networks in cache_scripts
- Solved some Aragon issues in cache_scripts ([#18](https://github.com/Grasia/dao-analyzer/issues/18))
- Now obtaining all DAOHaus DAO names ([#30](https://github.com/Grasia/dao-analyzer/issues/30))

## 0.5.4 - 2021-09-28
- Fixed #26 & #27
- Changed DAO selector label
- Changed DAO selector sorting method

## 0.5.3 - 2021-09-22
- Fixed #17
- Removed small jerk on hover of organization selector


## 0.5.2 - 2021-04-14
### Added
- Shows last updated date
### Changed
- DAOs now are case insensitive sorted
- DAOhaus is loaded by default

## 0.5.1 - 2021-01-28
### Added
- App icon
- Visual loading state during platform selection loading 
### Changed
- "All DAOs" are selected by default

## 0.5.0 - 2021-01-15
### Added
- New interface design
### Fixed
- DAOstack proposal metric bug

## 0.4.2 - 2020-11-06
### Added
- Added new metrics
### Changed
- Some endpoints
### Fixed
- Aragon vote collector bug

## 0.4.1 - 2020-11-03
### Added
- Added xdai DAOs for each platform
### Fixed
- Aragon vote outcome calculation

## 0.4.0 - 2020-10-23
### Added
- Scripts to download and update Aragon's data
- Aragon metrics:
    * Months which the DAO has registered activity (Also availables for DAOstack, and DAOhaus)
    * Active token holders
    * New votes
    * Votes's outcome
    * Casted votes by support
    * Active voters
    * New transactions
    * Installed apps

## 0.3.1 - 2020-10-14
### Added
- Small visual changes.

## 0.3.0 - 2020-10-09
### Added
- Compatibility with DAOhaus.
- New main view.
- Several metrics of DAOhaus DAOs. You can see them in the readme file.

## 0.2.1 - 2020-09-08
### Added
- Added licenses in the web page and acknowledgements

## 0.2.0 - 2020-08-24
### Added
- Graph of active users
### Fixed
- Bugs related with the cache script

## 0.1.0 - 2020-07-22
### Added

- Scripts to download and update DAOstack's data
- DAO selector or all of them
- Graphs:
    * New reputation holders
    * Total votes option
    * Different voters
    * Total stakes
    * Different stakers
    * New proposals
    * Closed proposal's majority outcome
    * Closed proposal's outcome
    * Total success rate of the stakes
    * Success rate of the stakes by type