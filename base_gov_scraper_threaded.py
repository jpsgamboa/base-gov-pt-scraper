import os
import requests
import sqlite3
import json
import re
import time
import threading
import contextlib

# options
_sqlite_location = None
_sqlite_name = None

_requests_range_step = 100
_max_number_of_threads = 5

# site info
_base_url = 'http://www.base.gov.pt/base2/rest/contratos'
_docs_url = 'http://www.base.gov.pt/base2/rest/documentos'

_contract_ids = []

# _db_conn = None
def get_db_connection():
    sqlite_path = os.path.join(_sqlite_location, _sqlite_name)
    _db_conn = sqlite3.connect(sqlite_path)
    return _db_conn

_range_limit = None
def get_range_limit():
    global _range_limit
    if _range_limit is None:
        try:
            r = requests.get(_base_url)
            content_range = r.headers['Content-Range']
            _range_limit = int(content_range.split('/')[1])  
        except:
            get_range_limit()
    return _range_limit
            
def get_contracts_request(from_range, to_range):    
    headers = {'Range': '{}-{}'.format(from_range, to_range)}
    return requests.get(_base_url, headers=headers, timeout=60).content.decode('utf-8')

def get_contract_ids_from_range_response(response):
    j = json.loads(response)
    return [contract['id'] for contract in j]

def get_contract(contract_id, timeout):
    r = requests.get("{}/{}".format(_base_url, contract_id),  timeout=timeout)
    res = r.content.decode('utf-8')
    return json.loads(res)

def get_last_requested_range(db_conn):
    cursor = db_conn.cursor()
    cursor.execute('SELECT to_range FROM scrape_history ORDER BY to_range DESC LIMIT 1')
    res = cursor.fetchone()
    cursor.close()
    if not res:
        return 0
    return res[0]

def get_incomplete_ranges(db_conn):
    cursor = db_conn.cursor()
    cursor.execute('SELECT from_range, to_range FROM scrape_history WHERE successful_count < contracts_count ORDER BY from_range')
    res = cursor.fetchall()
    cursor.close()
    if not res:
        return False

    ranges = []
    for r in res:
        ranges.append([r[0],r[1]])
    return ranges

def get_skipped_ranges(db_conn):
    cursor = db_conn.cursor()
    cursor.execute('select from_range, to_range from `scrape_history` order by from_range')
    res = cursor.fetchall()
    cursor.close()
    if not res:
        return False

    ranges = []
    for i, rng in enumerate(res):
        if i == (len(res) - 1): break
        
        tr = rng[1]
        next_fr = res[i+1][0]

        if tr != next_fr:
            remaining = next_fr - tr
            f = tr
            while (remaining > 0):
                t = f + min(100, remaining)
                ranges.append([f, t])
                remaining -= min(100, remaining)
                f = t

    return ranges

def contract_exists_in_db(contract_id):
    return contract_id in _contract_ids  

def load_contract_ids():
    c = get_db_connection()
    try:
        cursor = c.cursor()
        cursor.execute('SELECT contract_id FROM contracts')
        rows = cursor.fetchall()

        global _contract_ids
        _contract_ids = []
        for r in rows:
            _contract_ids.append(r[0])
        cursor.close()
        c.close()
    except Exception as e:
        print("Problem loading IDs: {}".format(e))

def add_contract_to_database(contract_id, contract_response, docs, db_conn):

    def normalizeCurrency(money):        
        if isinstance(money, str):
            normalized = money.replace('€','').replace('.','').strip().replace(' ', '').replace(',','.')
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
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE company_id = {0}'.format(company_id))
        res = cursor.fetchone()

        if not res: # doesn't exist
            sql = "INSERT INTO companies (company_id, description, nif) VALUES (?,?,?)"
            cursor.execute(sql, (company_id, description, nif))
        cursor.close()
    def add_contestant(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        db_conn.cursor().execute("INSERT INTO contestants(contract_id, company_id) VALUES (?,?)", (contract_id, company_id)).close()

    def add_contracted(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        db_conn.cursor().execute("INSERT INTO contracted(contract_id, company_id) VALUES (?,?)", (contract_id, company_id)).close()

    def add_contracting(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        db_conn.cursor().execute("INSERT INTO contracting(contract_id, company_id) VALUES (?,?)", (contract_id, company_id)).close()

    def add_invitee(contract_id, company_id, description, nif):
        add_company_if_not_exists(company_id, description, nif)
        db_conn.cursor().execute("INSERT INTO invitees(contract_id, company_id) VALUES (?,?)", (contract_id, company_id)).close()

    def add_document(contract_id, document_id, description, doc_content):       
        db_conn.cursor().execute("INSERT INTO documents VALUES(?,?,?,?)", ( contract_id, document_id , description, doc_content)).close()

    # Insert contract list parts
    for doc in docs:
        add_document(contract_id, doc[0], doc[1], doc[2])

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

    db_conn.cursor().execute(sql, values).close()
    
    # Finish
    #get_db_connection().commit()

def update_range_history_in_db(from_range, to_range, nr_contracts, successful_contracts, db_conn):
    cursor = db_conn.cursor()
    sql = "SELECT * FROM scrape_history WHERE from_range = ? AND to_range = ?"
    cursor.execute(sql, (from_range, to_range))
    res = cursor.fetchone()

    if not res:
        sql = "INSERT INTO scrape_history (from_range, to_range, contracts_count, successful_count) VALUES (?,?,?,?)"
        cursor.execute(sql, (from_range, to_range, nr_contracts, successful_contracts))
    else:
        sql = "UPDATE scrape_history SET successful_count = ? WHERE from_range = ? AND to_range = ?"
        cursor.execute(sql, (successful_contracts, from_range, to_range))
    cursor.close()
    #get_db_connection().commit()


def iterate_range(from_range, to_range, timeout, try_count = 0):
    print ("Range {0} - {1} Iterating: {2:.2f}%".format(from_range, to_range, from_range/get_range_limit()*100))
    successful_contracts_count = 0

    try:
        contract_list_response = get_contracts_request(from_range, to_range)
        contract_ids_list = get_contract_ids_from_range_response(contract_list_response)
    except Exception as e:
        print ("    ### Failure. Error getting contract range {0}-{1}. Error: {2}".format(from_range, to_range, e) )
        if try_count < 10:
            iterate_range(from_range, to_range, timeout, try_count + 1)
        return 

    contracts = []
    
    for contract_id in contract_ids_list:
        # print ("\rContract: {}".format(contract_id), end='')
        
        if contract_exists_in_db(contract_id):
            successful_contracts_count += 1
            continue

        try:
            contract_response = get_contract(contract_id, timeout)

            docs = []

            for doc in contract_response['documents']:
                doc_id = doc['id']
                doc_desc = doc['description']
                doc = requests.get("{}/{}".format(_docs_url, doc_id))  
                docs.append([doc_id, doc_desc, doc.content])

            contracts.append([contract_id, contract_response, docs])
        except Exception as e:
            # message = "    ### Failure. Error getting contract {0}. Error: {1}".format(contract_id, e)
            # if not "Read timed out" in str(message):
            #     print (message)
            continue

    # print("     Range {0} - {1} - completed".format(from_range, to_range))
    insert_contracts(contracts, from_range, to_range, len(contract_ids_list), successful_contracts_count)

_lock = threading.Lock()
def insert_contracts(contracts, from_range, to_range, len_ids, successful_contracts_count):
    _lock.acquire()
    # print("     Range {0} - {1} - begin inserting".format(from_range, to_range))
    try:
        with contextlib.closing(get_db_connection()) as db_conn:
            with db_conn:
                for contract in contracts:
                    try:
                        add_contract_to_database(contract[0], contract[1], contract[2], db_conn)
                        _contract_ids.append(contract[0])
                        successful_contracts_count += 1
                    except Exception as e:
                        # print ("    ### Failure. Error inserting contract {0}. Error: {1}".format(contract[0], e) )
                        continue
                
                del contracts

                update_range_history_in_db(from_range, to_range, len_ids, successful_contracts_count, db_conn)

    except Exception as e:
        print ("    ### Failure. Error inserting contracts of range {0} - {1}. Error: {2}".format(str(from_range), str(to_range), e) )
    finally:
        # print("     Range {0} - {1} - end inserting: {2}/{3}".format(from_range, to_range, successful_contracts_count, len_ids))
        _lock.release()

def iter_past():
    with contextlib.closing(get_db_connection()) as c:
        incomplete_ranges = get_incomplete_ranges(c) + get_skipped_ranges(c)

    if incomplete_ranges == False: return

    print("\n\nRepeating incomplete ranges: {}\n\n".format(len(incomplete_ranges)))

    threads = []
    iter_count = 0
    while iter_count < len(incomplete_ranges):
        if len(threads) >= _max_number_of_threads:
            for t in threads: 
                if not t.is_alive(): 
                    t.join()
            threads = [t for t in threads if t.is_alive()]
            continue

        rng = incomplete_ranges[iter_count]

        t = threading.Thread(target=iterate_range, args=(rng[0], rng[1], 120))
        t.start()
        threads.append(t)

        iter_count += 1
        time.sleep(.2)

    # join threads
    for t in threads:
        t.join()

    completed = False
    with contextlib.closing(get_db_connection()) as c:
        completed = get_incomplete_ranges(c) == False
    return completed
    
def iter_next():
    range_limit = get_range_limit()
    with contextlib.closing(get_db_connection()) as c:
        range_start = get_last_requested_range(c)
    
    print("\n\nGetting new ranges starting from: {}\n\n".format(range_start))

    threads = []

    iter_count = 0
    while range_start <= range_limit:
        if len(threads) >= _max_number_of_threads:
            for t in threads: 
                if not t.is_alive(): 
                    t.join()
            threads = [t for t in threads if t.is_alive()]
            continue
        
        step = min([_requests_range_step, range_limit - range_start])

        t = threading.Thread(target=iterate_range, args=(range_start, range_start + step, 1))
        t.start()
        threads.append(t)

        iter_count += 1

        if iter_count > 7:
            break

        range_start += step 
        time.sleep(.2)
    
    # join threads
    for t in threads:
        t.join()

    return range_start == range_limit
        

def main(sqlite_location, sqlite_name):
    global _sqlite_location
    global _sqlite_name

    _sqlite_location = sqlite_location 
    _sqlite_name = sqlite_name

    load_contract_ids()

    to_continue = True
    while(to_continue):
        next_complete = iter_next()
        past_complete = iter_past()
        to_continue = not past_complete or not next_complete

if __name__ == '__main__':

    sqlite_location = os.path.dirname(os.path.abspath(__file__)) 
    sqlite_name = "BaseGovData.db"

    main(sqlite_location, sqlite_name)