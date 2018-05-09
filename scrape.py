import requests
import sqlite3
import os
import csv
import pandas as pd 
import datetime
import io
from random import randint
import time


def get_url(from_date, to_date):
    return ("http://www.base.gov.pt/base2/rest/contratos.csv?texto=&tipo=0&tipocontrato=0"
            "&cpv=&numeroanuncio=&aqinfo=&adjudicante=&adjudicataria=&desdeprecocontrato_false="
            "&desdeprecocontrato=&ateprecocontrato_false=&ateprecocontrato="
            "&desdedatacontrato={0}&atedatacontrato={1}"
            "&desdedatapublicacao=&atedatapublicacao=&desdeprazoexecucao=&ateprazoexecucao="
            "&desdedatafecho=&atedatafecho=&desdeprecoefectivo_false=&desdeprecoefectivo="
            "&ateprecoefectivo_false=&ateprecoefectivo=&pais=0&distrito=0&concelho=0&sort(-publicationDate)").format(from_date, to_date)

base_path = os.path.dirname(os.path.abspath(__file__)) 
sqlite_path = os.path.join(base_path, "BaseGovData.db")

default_fetch_interval = 2
fetch_interval = default_fetch_interval

conn = sqlite3.connect(sqlite_path)

# check if any records
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM contratos')
count = cursor.fetchone()[0]

if count > 0:

    # get latest insert date
    cursor = conn.cursor()
    cursor.execute('SELECT _insertdate FROM contratos ORDER BY _id DESC LIMIT 1')
    d = cursor.fetchone()[0]

    last_insert_date = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

    sdate = (last_insert_date + datetime.timedelta(days=1))

else:
    sdate = datetime.datetime.strptime("2008-01-01", "%Y-%m-%d") 

edate = sdate + datetime.timedelta(days=fetch_interval)

while edate <= (datetime.datetime.now() - datetime.timedelta(days=1)):
    edate = sdate + datetime.timedelta(days=fetch_interval)

    print ("Request at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  + ":   " + sdate.strftime("%Y-%m-%d") + " to " + edate.strftime("%Y-%m-%d"))

    url = get_url(sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"))

    try:
        r = requests.get(url, timeout =300)
    except Exception as e:
        print ("    ### Failure. Could not connect. Retying in 5 seconds. Error: {0}".format(e) )
        time.sleep(5)
        continue

    data = r.content.decode('utf-8')

    if r.status_code >= 500:
        new_interval = fetch_interval - 1
        fetch_interval = new_interval if new_interval >= 0 else default_fetch_interval
        print ("    ### Failure. No data returned. Retying with interval of {0} days. Status: {1}".format(fetch_interval, r.status_code) )
        continue
    
    try:
        df = pd.read_csv(io.StringIO(data), sep=";")

        df['_insertdate'] = edate

        df.columns = df.columns.str.replace('\s+', '')

        df.to_sql("contratos", conn, if_exists="append", index=False)

    except:
        fetch_interval = randint(1,30)        
        print ("    ### Failure. Error parsing or inserting data. Retying with interval of {0} days. Status:{1}, Data:\n{2}".format(fetch_interval, r.status_code, data) )
        continue

    sdate = edate + datetime.timedelta(days=1)
    fetch_interval = default_fetch_interval

conn.close()