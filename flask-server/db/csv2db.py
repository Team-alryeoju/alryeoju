# -*- coding:utf-8 -*-
import csv
import sqlite3


#database에 연결
conn = sqlite3.connect('alryeoju.db')

#cursor 객체를 만들고 실행
cursor = conn.cursor()

#테이블 정의 - 테이블이 없을 경우
#create_table = '''CREATE TABLE sool_(alname text, alid integer, img_url text);'''
    
#db에 정의된 테이블 생성 - 테이블 생성
#cursor.execute(create_table)

#csv파일 오픈
file = open('buy_info.csv',encoding='utf-8-sig')
contents = csv.reader(file)

insert_records = 'INSERT INTO buy_info(al_id, u_id, datetime) values (?,?,?)'
cursor.executemany(insert_records, contents)

select_all = "SELECT * FROM buy_info"
rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

conn.commit()
conn.close()

    