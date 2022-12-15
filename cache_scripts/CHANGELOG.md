# Changelog
All notable changes to this project will be documented in this file.

## 1.1.7 - 2022-12-13
- Obtaining more fields from DAOstack proposals
  - queuedVotePeriodLimit
  - boostedVotePeriodLimit

## 1.1.6 - 2022-10-22
- Obtaining more time fields from DAOstack proposals

## 1.1.5 - 2022-10-17
- Remove DAOstack phantom DAOs [#120](https://github.com/Grasia/dao-analyzer/issues/120)
- Added option to obtain non-registered DAOs from DAOstack (`--daostack-all`)

## 1.1.4 - 2022-07-15
- Added postProcessor to add a `dao` field to reputation mints and burns
- Not getting reputation mints/burns of amount 0 (not useful)

## 1.1.3 - 2022-07-11
- Added competitionId to daostack proposals

## 1.1.2 - 2022-06-29
- Added ReputationMint and ReputationBurn collectors to DAOstack

## 1.1.1 - 2022-06-10
- Added originalCreator field to Aragon Voting subgraph

## 1.1.0 - 2022-05
- Used `_change_block` filter to make every subgraph updatable
- Fixed cryptocompare error
- Fixed requests to `_blocks` endpoint 
- Added --skip-token-balances option to cli

## 1.0.3 - 2022-03-24
- Obtaining assets of DAOs
- Added BlockScout balances collector
- Added CryptoCompare token prices collector
- Some changes on Class sctructure