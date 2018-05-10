import os
import requests
import sqlite3
import json
import re
import time

# options
requests_range_step = 100
sqlite_location = os.path.dirname(os.path.abspath(__file__)) 
sqlite_name = "BaseGovData.db"

# site info
base_url = 'http://www.base.gov.pt/base2/rest/contratos'
docs_url = 'http://www.base.gov.pt/base2/rest/documentos'

# global
_db_conn = None
def get_db_connection():
    global _db_conn
    if _db_conn is None:
        sqlite_path = os.path.join(sqlite_location, "BaseGovData.db")
        _db_conn = sqlite3.connect(sqlite_path)
    return _db_conn

_range_limit = None
def get_range_limit():
    global _range_limit
    if _range_limit is None:
        _range_limit = 868250 # TODO    
    return _range_limit

def get_contracts_request(from_range, to_range):    
    headers = {'Range': '{}-{}'.format(from_range, to_range)}
    return requests.get(base_url, headers=headers).content.decode('utf-8')

def get_contract_ids_from_range_response(response):
    j = json.loads(response)
    return [contract['id'] for contract in j]

def get_contract(contract_id):
    r = requests.get("{}/{}".format(base_url, contract_id))
    res = r.content.decode('utf-8')
    return json.loads(res)

def get_last_requested_range():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT to_range FROM scrape_history ORDER BY id DESC LIMIT 1')
    res = cursor.fetchone()
    if not res:
        return 0
    return res[0]

def get_incomplete_range():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT from_range, to_range FROM scrape_history WHERE successful_count < contracts_count LIMIT 1')
    res = cursor.fetchone()
    if not res:
        return False
    return [res[0],res[1]]

def contract_exists_in_db(contract_id):
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT * FROM contracts WHERE contract_id = {0}'.format(contract_id))
    res = cursor.fetchone()    
    if not res:
        return False
    return True

def add_contract_to_database(contract_id, contract_response):

    def normalizeCurrency(money):
        if money is not None:
            normalized = re.sub(r'^((\d+)\.)?(\d+),(\d+) €$', r'\2\3.\4', money)
        else:
            normalized = 0.0
        return float(normalized)

    def location_tuple(location):
        if location is None: location = ""
        parts = [p.strip() for p in location.split(",")]
        for p in range(len(parts), 3):
            parts.append("")
        return parts

    def add_company_if_not_exists(company_id, description, nif):
        # Check if exists
        cursor = get_db_connection().cursor()
        cursor.execute('SELECT * FROM companies WHERE company_id = {0}'.format(company_id))
        res = cursor.fetchone()

        if not res: # doesn't exist
            sql = "INSERT INTO companies (company_id, description, nif) VALUES (?,?,?)"
            cursor.execute(sql, (company_id, description, nif))

    def add_contestant(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        get_db_connection().cursor().execute("INSERT INTO contestants(contract_id, company_id) VALUES (?,?)", (contract_id, company_id))

    def add_contracted(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        get_db_connection().cursor().execute("INSERT INTO contracted(contract_id, company_id) VALUES (?,?)", (contract_id, company_id))

    def add_contracting(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        get_db_connection().cursor().execute("INSERT INTO contracting(contract_id, company_id) VALUES (?,?)", (contract_id, company_id))

    def add_invitee(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        get_db_connection().cursor().execute("INSERT INTO invitees(contract_id, company_id) VALUES (?,?)", (contract_id, company_id))

    def add_document(contract_id, document_id, description):       
        r = requests.get("{}/{}".format(docs_url, document_id))        
        get_db_connection().cursor().execute("INSERT INTO documents VALUES(?,?,?,?)", ( contract_id, document_id , description, r.content))


    # Insert contract list parts
    for doc in contract_response['documents']:
        add_document(contract_id, doc['id'], doc['description'])

    for contestant in contract_response['contestants']:
        add_contestant(contract_id, contestant['id'], contestant['description'], contestant['nif'])

    for invitee in contract_response['invitees']:
        add_invitee(contract_id, invitee['id'], invitee['description'], invitee['nif'])

    for contracting in contract_response['contracting']:
        add_contracting(contract_id, contracting['id'], contracting['description'], contracting['nif'])

    for contracted in contract_response['contracted']:
        add_contracted(contract_id, contracted['id'], contracted['description'], contracted['nif'])
    
    # Insert single parts
    sql = """INSERT INTO contracts (
                        contract_id,
                        announcement_id,
                        description,
                        brief_description,
                        signing_date,
                        close_date,
                        publication_date,
                        contract_type,
                        procedure_type,
                        execution_deadline,
                        contract_fundamentation,
                        direct_award_fundamentarion,
                        contract_status,
                        centralized_procedure,
                        initial_contractual_price,
                        total_effective_price,
                        cpvs,
                        country,
                        municipality,
                        parish,
                        price_change_cause,
                        deadline_change_cause,
                        observations,
                        framework_agreement_proc_id,
                        framework_agreement_proc_desc,
                        increments 
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """

    values = (
        contract_response['id'],
        contract_response['announcementId'],
        contract_response['description'],
        contract_response['objectBriefDescription'],
        contract_response['signingDate'],
        contract_response['closeDate'],
        contract_response['publicationDate'],
        contract_response['contractTypes'],
        contract_response['contractingProcedureType'],
        contract_response['executionDeadline'],
        contract_response['contractFundamentationType'],
        contract_response['directAwardFundamentationType'],
        contract_response['contractStatus'],
        contract_response['centralizedProcedure'],
        normalizeCurrency(contract_response['initialContractualPrice']),
        normalizeCurrency(contract_response['totalEffectivePrice']),
        contract_response['cpvs'],
        location_tuple(contract_response['executionPlace'])[0],
        location_tuple(contract_response['executionPlace'])[1],
        location_tuple(contract_response['executionPlace'])[2],
        contract_response['causesPriceChange'],
        contract_response['causesDeadlineChange'],
        contract_response['observations'],
        contract_response['frameworkAgreementProcedureId'],
        contract_response['frameworkAgreementProcedureDescription'],
        contract_response['increments']
    )

    get_db_connection().cursor().execute(sql, values)
    
    # Finish
    get_db_connection().commit()

def update_range_history_in_db(from_range, to_range, nr_contracts, successful_contracts):
    cursor = get_db_connection().cursor()
    sql = "SELECT * FROM scrape_history WHERE from_range = ? AND to_range = ?"
    cursor.execute(sql, (from_range, to_range))
    res = cursor.fetchone()

    if not res:
        sql = "INSERT INTO scrape_history (from_range, to_range, contracts_count, successful_count) VALUES (?,?,?,?)"
        cursor.execute(sql, (from_range, to_range, nr_contracts, successful_contracts))
    else:
        sql = "UPDATE scrape_history SET successful_count = ? WHERE from_range = ? AND to_range = ?"
        cursor.execute(sql, (successful_contracts, from_range, to_range))
    
    get_db_connection().commit()

def iterate_range(from_range, to_range):
    print ("Iterating range {0} - {1}: {2:.2f}%".format(from_range, to_range, from_range/get_range_limit()*100))

    try:
        contract_list_response = get_contracts_request(from_range, to_range)
        contract_ids_list = get_contract_ids_from_range_response(contract_list_response)
    except Exception as e:
            print ("    ### Failure. Error getting contract range {0}-{1}. Error: {2}".format(from_range, to_range, e) )
            return False

    successful_contracts_count = 0
    
    for contract_id in contract_ids_list:
        print ("\rContract: {}".format(contract_id), end='')
        

        if contract_exists_in_db(contract_id):
            successful_contracts_count += 1
            continue

        try:
            contract_response = get_contract(contract_id)
            time.sleep(0.2)
        except Exception as e:
            print ("    ### Failure. Error getting contract {0}. Error: {1}".format(contract_id, e) )
            continue

        try:
            add_contract_to_database(contract_id, contract_response)
        except Exception as e:
            print ("    ### Failure. Error inserting contract {0}. Error: {1}".format(contract_id, e) )
            continue

        successful_contracts_count += 1    

    print("")

    update_range_history_in_db(from_range, to_range, len(contract_ids_list), successful_contracts_count)

    return True

def iter_past():
    rng = get_incomplete_range()
    while not isinstance(rng, bool):
        iterate_range(rng[0], rng[1], )

        rng = get_incomplete_range()

def iter_next():
    range_limit = get_range_limit()
    range_start = get_last_requested_range()
    
    while range_start < range_limit:
        step = min([requests_range_step, range_limit - range_start])

        result = iterate_range(range_start, range_start + step)

        if result == True:
            range_start += step 
        
        iter_past() # make another pass to try and insert the ones that failed


def main():    
    iter_next()



if __name__ == '__main__':
    main()

