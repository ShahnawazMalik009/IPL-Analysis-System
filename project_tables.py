import sqlite3
conobj=sqlite3.connect(database="Banking.sqlite")
cursorobj=conobj.cursor()

try:
    table_users=''' create table users(users_acno integer primary key autoincrement,
    users_name text,users_pass text,users_mob text,users_email text,users_bal text,users_aadar text,
    users_opendate text)
    '''
    
    table_transaction=''' create table txn(txn_id integer primary key autoincrement,
    txn_acno int,txn_type text,txn_amt float,txn_bal float,txn_date text)
    '''
    cursorobj.execute(table_users)
    cursorobj.execute(table_transaction)
    print("table created")
    
except Exception as e:
    print(e)    
finally:
    conobj.close()    
    
    #amny uodf vqmr nsgb 