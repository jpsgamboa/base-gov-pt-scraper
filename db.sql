BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `scrape_history` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`from_range`	INTEGER,
	`to_range`	INTEGER,
	`contracts_count`	INTEGER,
	`successful_count`	INTEGER
);
CREATE TABLE IF NOT EXISTS `invitees` (
	`contract_id`	INTEGER,
	`company_id`	INTEGER
);
CREATE TABLE IF NOT EXISTS `documents` (
	`contract_id`	INTEGER,
	`document_id`	INTEGER,
	`description`	TEXT,
	`file`	BLOB
);
CREATE TABLE IF NOT EXISTS `contracts` (
	`contract_id`	INTEGER,
	`announcement_id`	INTEGER,
	`description`	TEXT,
	`brief_description`	TEXT,
	`signing_date`	TEXT,
	`close_date`	NUMERIC,
	`publication_date`	TEXT,
	`contract_type`	TEXT,
	`procedure_type`	TEXT,
	`execution_deadline`	INTEGER,
	`contract_fundamentation`	TEXT,
	`direct_award_fundamentation`	TEXT,
	`contract_status`	TEXT,
	`centralized_procedure`	TEXT,
	`initial_contractual_price`	REAL,
	`total_effective_price`	REAL,
	`cpvs`	TEXT,
	`country`	TEXT,
	`municipality`	TEXT,
	`parish`	TEXT,
	`price_change_cause`	TEXT,
	`deadline_change_cause`	TEXT,
	`observations`	TEXT,
	`framework_agreement_proc_id`	TEXT,
	`framework_agreement_proc_desc`	TEXT,
	`increments`	TEXT
);
CREATE TABLE IF NOT EXISTS `contracting` (
	`contract_id`	INTEGER,
	`company_id`	INTEGER
);
CREATE TABLE IF NOT EXISTS `contracted` (
	`contract_id`	INTEGER,
	`company_id`	INTEGER
);
CREATE TABLE IF NOT EXISTS `contestants` (
	`contract_id`	INTEGER,
	`company_id`	INTEGER
);
CREATE TABLE IF NOT EXISTS `companies` (
	`company_id`	INTEGER,
	`description`	TEXT,
	`nif`	TEXT
);
COMMIT;
