import pandas as pd
import psycopg2
import getpass


def connect(initfile='database.ini'):
    with open('./database.ini', 'r') as fd:
        params = fd.read().replace('\n', ' ')
        with_password = False
        
        # check if password is in params
        for p in params.split(' '):
            if p.startswith('password='):
                with_password = True
        # if not ask for password
        if not with_password:
            password = getpass.getpass()
            params += ' password=' + password
    try:
        db_con = psycopg2.connect(params)
    except Exception as error:
        print(error)
        p = params.split(' ')
        for s in p:
            if s.startswith('password='):
                p.remove(s)
        print('unable to connect to:\n', p)
        exit()
    return db_con


sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"


if __name__ == '__main__':
    q1 = ''
    q2 = ''
    with open('./create.sql', 'r') as fd:
        q1 = fd.read()
    with open('./populate.sql', 'r') as fd:
        q2 = fd.read()
    with connect() as db_con:
        cur = db_con.cursor()
        cur.execute(q1) 
        cur.execute(q2)
        cur.execute('SELECT * FROM location')
        res = cur.fetchall()
        for row in res:
            print('city_id: ', row[0])
            print('city_name: ', row[1])
            print('locality: ', row[2])
            print('country: ', row[3])
            print('\n')
        db_con.commit()


