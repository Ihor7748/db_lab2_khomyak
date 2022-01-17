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
    q1 = 'select comodity, price from market natural join comodity_price where market_id=1871;'
    q2 = 'select country_name, count(country_name) from location natural join market group by country_name;'
    q3 = "select year, price from market natural join comodity_price natural join location where country_name='Ukraine' and comodity='Potatoes - Retail'"
    with connect() as db_con:
        cur = db_con.cursor()
        cur.execute(q1) 
        res = cur.fetchall()
        print('ціни на продукти на ринку львова')
        for row in res:
            print('commodity: ', row[0])
            print('price: ', row[1])
        cur.execute(q2)
        res = cur.fetchall()
        print('кількість ринків країни в нашій базі данних:')
        for row in res:
            print('country_name: ', row[0])
            print('count: ', row[1])
        cur.execute(q3)
        res = cur.fetchall()
        print('ціни на картоплю в україні з роками')
        for row in res:
            print('year: ', row[0])
            print('count: ', row[1])

        


