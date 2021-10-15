# Changelog
All notable changes to this project will be documented in this file.

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