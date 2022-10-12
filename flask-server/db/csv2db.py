import csv
import sqlite3


#database에 연결
conn = sqlite3.connect('test.db')

#cursor 객체를 만들고 실행
cursor = conn.cursor()

#테이블 정의
#create_table = '''CREATE TABLE sool_(alname text, alid integer, img_url text);'''
    
#db에 정의된 테이블 생성
#cursor.execute(create_table)

#csv파일 오픈
file = open('test.csv',encoding='utf-8-sig')
#C:\Users\taeyeon\Desktop\asdfasdf\asdfasdf\test.csv
#asdfasdf\test.csv
contents = csv.reader(file)

insert_records = 'INSERT INTO h1(name, id, img_url) values(?,?,?)'

cursor.executemany(insert_records, contents)

select_all = "SELECT * FROM h1"
rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

conn.commit()
conn.close()

    