#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import pymysql
from randm import num, strng

con = pymysql.connect(host='localhost',
                      user='root',
                      password='1234',
                      database='learn',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()
args = sys.argv
if len(args) == 1:
    print(f'Please, set argument! Type "{args[0]} help" for get help')
else:
    if args[1] == 'help':
        print("""
        create - Create DB's
        delete - Delete DB's
        insert [test1/test2] [size] - Insert random rows (count of row = size) data to table "test1" or "test2"
        clear [test1/test2] - Clear DB values
        get [test1/test2] - Get table values
        merge - Merge test1 and test2 tables
        """)

    if args[1] == 'create':
        with con:
            cur.execute(
                "CREATE TABLE test1(id INT NOT NULL AUTO_INCREMENT, uniqeId VARCHAR(32), age INT,email VARCHAR(64), PRIMARY KEY(id))")
            cur.execute(
                "CREATE TABLE test2(id INT NOT NULL AUTO_INCREMENT, uniqeId VARCHAR(32), address VARCHAR(32), orderId INT,product INT,date_time DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))")
            print("Test DB's created")

    if args[1] == 'delete':
        with con:
            cur.execute("DROP TABLE test1")
            cur.execute("DROP TABLE test2")
            print("Test DB's dropped")

    if args[1] == 'insert':
        if len(args) == 4:
            with con:
                if args[2] == "test1":
                    for i in range(int(args[3])):
                        cur.execute(f"INSERT INTO test1(uniqeId,age,email) VALUES(\"{strng(32)}\",{num()},\"{strng(16)}\");")
                        con.commit()
                    print("Successfully insert into test1!")
                elif args[2] == "test2":
                    for i in range(int(args[3])):
                        cur.execute(f'INSERT INTO test2(uniqeId,address,orderId,product) VALUES("{strng(32)}","{strng(6)}",{num()},{num()});')
                        con.commit()
                    print("Successfully insert into test2!")
                else:
                    print("Unknown argument")
        else:
            print("insert [test1/test2] [count]")

    if args[1] == 'clear':
        if len(args) == 3:
            with con:
                if args[2] == "test1":
                    cur.execute('TRUNCATE test1')
                    print("test1 is clear")
                elif args[2] == "test2":
                    cur.execute('TRUNCATE test2')
                    print("test1 is clear")
                else:
                    print("Unknown argument")
        else:
            print("clear [test1/test2]")

    if args[1] == 'get':
        if len(args) == 3:
            with con:
                if args[2] == "test1":
                    cur.execute('SELECT * FROM test1')
                    for row in cur.fetchall():
                        print(str(row['id'])+' ' + row['uniqeId']+ ' ' + row['email'])
                elif args[2] == "test2":
                    cur.execute('SELECT * FROM test2')
                    for row in cur.fetchall():
                        print(row['uniqeId']+row['address']+' ' + str(row['orderId']) + ' ' + str(row['product']) + ' ' + str(row['date_time']))
                else:
                    print("Unknown argument")
        else:
            print("get [test1/test2]")
    if args[1] == 'merge':
        cur.execute("""
SELECT test1.id,test1.uniqeId,test1.age,test1.email,test2.address,test2.orderId,test2.product,test2.date_time FROM test1
LEFT JOIN test2
ON test1.uniqeId = test2.uniqeId""")
        cur.execute("SELECT DISTINCT test2.uniqeId  FROM test1, test2 WHERE test1.uniqeId<>test2.uniqeId")
        rows = cur.fetchall()
        for row in rows:
            cur.execute(f'INSERT INTO test1(uniqeId) VALUE("{row["uniqeId"]}")')

        con.commit()
### Don't work at MariaDB ####
#         cur.execute("""SELECT * FROM test1
# MERGE test1 AS Target
# USING test2 AS Source
#     ON (Target.uniqeId = Source.uniqeId)
# WHEN MATCHED
#     THEN UPDATE
#         SET SalesCount = Source.SalesCount
# WHEN NOT MATCHED
#     THEN INSERT
#         VALUES (Source.address, Source.orderId, Source.productm,Source.date_time)""")



