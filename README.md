# Base.gov.pt Scraper

A python script to download all contracts from [base.gov.pt](http://www.base.gov.pt/Base/pt/Homepage) into a SQLite database.

The script creates an SQLite database to store the contracts and associated attributes:

|Tables     |Description                            |Key
|-----------|:-------------------------------------:|:---------------------------:|
|contracts  |Contracts information                  |`contract_id`                |
|companies  |Companies information                  | `company_id`                |
|contestants|Ids of the contestants of each contract| `contract_id`, `company_id` |
|contracted |Id(s) of the contracted company(ies)   | `contract_id`, `company_id` |
|contracting|Id of the contracting company          | `contract_id`, `company_id` |
|invitees   |Id(s) of the invited company(ies)      | `contract_id`, `company_id` |
|documents  |Documents associated with the contract | `contract_id`, `document_id`|

Takes a few days to run, so be patient.


## Usage:

```ps
Base.gov.pt scraper [-h] [-p DB_PATH] [-n DB_NAME] [-d DL_DOCS]

optional arguments:
  -h, --help            
  -p DB_PATH,  Location to store the database
  -n DB_NAME,  Name of the database
  -d DL_DOCS,  Option to download contract documents (True/False)
```
If not specified, by default the database will be store in the script's location.

It's possible to stop and resume the script at any time.

## Example

```ps
python base_gov_scraper.py -p "C:\base-gov-data" -n "base-gov.db" -d True
```

## Warning

By default (or using the option `-d True`) the program will download all the documents associated with the contract into the `documents` table.
This results in a very large database.
Use the option  `-d False` to skip downloading the documents.
