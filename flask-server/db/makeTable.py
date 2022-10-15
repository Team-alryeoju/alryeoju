from os import curdir
import sqlite3

#test.db 데이터베이스에 SQLite DB를 연결
conn = sqlite3.connect('alryeoju.sqlite')

conn.execute(
    '''
    create table user_profile(
	u_id integer,
	감칠맛 REAL,
	걸쭉함 REAL,
	견과류_땅콩_잣향 REAL,
	고소함 REAL,
	곡물_옥수수_보리 REAL,
	기타_커피_캐러멜_토란 REAL,
	깔끔 REAL,
	꿀맛_당류 REAL,
	누룩 REAL,
	다양 REAL,
	단맛 REAL,
	독특 REAL,
	드라이 REAL,
	레몬_유자류_감귤류_자몽 REAL,
	매실류_파인애플 REAL,
	바나나_망고_멜론 REAL,
	바닐라_국화_매화_연꽃_유채꽃_꽃향 REAL,
	베리류_딸기 REAL,
	사과_배_감 REAL,
	스모키한 REAL,
	신맛 REAL,
	여운 REAL,
	열대과일 REAL,
	오디_복분자 REAL,
	오미자류 REAL,
	음료 REAL,
	인삼_생강강황_약재 REAL,
	자두_복숭아_체리 REAL,
	잔잔한 REAL,
	조화 REAL,
	진득 REAL,
	청_포도 REAL,
	청량 REAL,
	탄닌감 REAL,
	탄산 REAL,
	풀내음_나무_볏짚 REAL,
	허브_시트러스 REAL,
	화끈함 REAL,
	constraint user_profile_fk foreign key(u_id) references users(u_id)
    )
    '''
)

conn.execute(
'''
create table item_profile(
	al_id integer,
	감칠맛 REAL,
	걸쭉함 REAL,
	견과류_땅콩_잣향 REAL,
	고소함 REAL,
	곡물_옥수수_보리 REAL,
	기타_커피_캐러멜_토란 REAL,
	깔끔 REAL,
	꿀맛_당류REAL,
	누룩 REAL,
	다양 REAL,
	단맛 REAL,
	독특 REAL,
	드라이 REAL,
	레몬_유자류_감귤류_자몽 REAL,
	매실류_파인애플 REAL,
	바나나_망고_멜론 REAL,
	바닐라_국화_매화_연꽃_유채꽃_꽃향 REAL,
	베리류_딸기 REAL,
	사과_배_감 REAL,
	스모키한 REAL,
	신맛 REAL,
	여운 REAL,
	열대과일 REAL,
	오디_복분자 REAL,
	오미자류 REAL,
	음료 REAL,
	인삼_생강강황_약재 REAL,
	자두_복숭아_체리 REAL,
	잔잔한 REAL,
	조화 REAL,
	진득 REAL,
	청_포도 REAL,
	청량 REAL,
	탄닌감 REAL,
	탄산 REAL,
	풀내음_나무_볏짚 REAL,
	허브_시트러스 REAL,
	화끈함 REAL,
	constraint item_profile_fk foreign key(al_id) references item_info(al_id)
    )
'''
)

conn.execute(
'''
create table reviews(
	u_id integer,
	u_name varchar(20),
	score real,
	datetime text,
	constraint reviews_fk foreign key(u_id) references users(u_id)
)
'''
)
conn.execute(
'''
create table users(
    u_id integer primary key autoincrement,
	user_sign_id  varchar(30) unique not null,
	user_sign_pw varchar(50),
	u_name varchar(10) unique
)
'''
)

conn.execute(
'''
create table item_info(
	al_id integer primary key autoincrement,
	al_name varchar(50),
	img_link text,
	detail text
)
'''
)
conn.execute(
'''
create table buy_info(
	al_id integer,
	u_id integer,
	datetime text,
	constraint buy_info_uid_fk foreign key(u_id) references users(u_id),
	constraint buy_info_alid_fk foreign key(al_id) references item_info(al_id)
)
'''
)
print('create table')


conn.close()


