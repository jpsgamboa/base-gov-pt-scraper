import requests
import sqlite3
import os
import csv
import pandas as pd 
import datetime
import io

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

fetch_interval_days = 30

conn = sqlite3.connect(sqlite_path)

# check if any records
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM contratos')
count = cursor.fetchone()[0]

edate = datetime.datetime.strptime("2008-01-01", "%Y-%m-%d") 

while edate < (datetime.datetime.now - datetime.timedelta(days=1)):

    if count > 0:

        # get latest insert date
        cursor = conn.cursor()
        cursor.execute('SELECT _insertdate FROM contratos ORDER BY _id DESC LIMIT 1')

        last_insert_date = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d")

        sdate = (last_insert_date + datetime.timedelta(days=1))

    else:
        sdate = datetime.datetime.strptime("2008-01-01", "%Y-%m-%d") 

    edate = sdate + datetime.timedelta(days=fetch_interval_days)

    url = get_url(sdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d"))

    r = requests.get(url)
    data = r.content.decode('utf-8')

    df = pd.read_csv(io.StringIO(data), sep=";")

    df['_insertdate'] = edate

    df.columns = df.columns.str.replace('\s+', '')

    df.to_sql("contratos", conn, flavor="sqlite", if_exists="append", index=False)

    print (sdate, edate)

conn.close()