import pandas as pd
import psycopg2
import getpass
from matplotlib import pyplot as plt


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




if __name__ == '__main__':
    q1 = 'select comodity, price from market natural join comodity_price where market_id=1871;'
    q2 = 'select country_name, count(country_name) from location natural join market group by country_name;'
    q3 = "select year, avg(price) from market natural join comodity_price natural join location where country_name='Ukraine' and comodity='Potatoes - Retail' group by year"
    with connect() as db_con:
        cur = db_con.cursor()
        cur.execute(q1) 
        res = cur.fetchall()
        lst = []
        lst2 = []
        for i in res:
            lst.append(float(i[1]))
            lst2.append(i[0])
        plt.bar(lst2, lst)
        plt.show()        
        cur.execute(q2)
        res = cur.fetchall()
        lst = []
        lst2 = []
        for i in res:
            lst.append(float(i[1]))
            lst2.append(i[0])
        plt.pie(lst, labels=lst2)
        plt.show()
        cur.execute(q3)
        res = cur.fetchall()
        lst = []
        lst2 = []
        for i in res:
            lst.append(int(i[0]))
            lst2.append(float(i[1]))
        plt.plot( lst, lst2)
        plt.show()



