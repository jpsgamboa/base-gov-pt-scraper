# Base.gov.pt Scraper

A python script to download all contracts from [base.gov.pt](http://www.base.gov.pt/Base/pt/Homepage) into a SQLite database.

The script creates an SQLite database to store the contracts and associated attributes:

|Tables     |Description                            |Key
|-----------|:-------------------------------------:|:---------------------------:|
|contracts  |Contract information                   |`contract_id`                |
|companies  |Company names                          | `company_id`                |
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
  -h, --help            show this help message and exit
  -p DB_PATH, --db_path DB_PATH Location for the database
  -n DB_NAME, --db_name DB_NAME Name for the database
  -d DL_DOCS, --dl_docs DL_DOCS Option to download contract documents
```

## Example

```ps
python base_gov_scraper.py -p "C:\base-gov-data" -n "base-gov.db" -d True
```

## Warning

By default (or using the option `-d True`) will download all the documents associated with the contract into the `documents` table.
This results in a very large database.
Use the option  `-d False` to skip downloading the documents.
