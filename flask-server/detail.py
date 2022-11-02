import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

token_list = ['감칠맛', '걸쭉함', '견과류_땅콩_잣향', '고소함', '곡물_옥수수_보리', '기타_커피_캐러멜_토란',
            '깔끔', '꿀맛_당류', '누룩', '다양', '단맛', '독특', '드라이', '레몬_유자류_감귤류_자몽',
            '매실류_파인애플', '바나나_망고_멜론', '바닐라_국화_매화_연꽃_유채꽃_꽃향', '베리류_딸기', '사과_배_감',
            '스모키한', '신맛', '여운', '열대과일', '오디_복분자', '오미자류', '음료', '인삼_생강강황_약재',
            '자두_복숭아_체리', '잔잔한', '조화', '진득', '청_포도', '청량', '탄닌감', '탄산', '풀내음_나무_볏짚',
            '허브_시트러스', '화끈함']

# 디테일 페이지 만들기
class detail_info:
    def __init__(self, cid, alid):
        #Mac용
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        # window  :  mac도 가능한가 확인 좀,,
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.c_id = cid
        self.al_id = alid
        query = "select img_link from item_info where al_id = " + str(alid)
        user_token = self.cursor.execute(query).fetchone()
        self.img_link = user_token[0]
        
    # 사용자 별 토큰 값 가져오기
    def select_user_token(self, c_id):
        query = "select * from user_profile where u_id=" +  str(c_id)
        user_token = self.cursor.execute(query).fetchall()
        # 리스트 타입 반환
        df = pd.DataFrame(data = {'tokens':user_token[0][1:]}).replace('', 0)
        df.index = token_list
        return df
    
    # 아이템 별 토큰 값 가져오기
    def select_al_token(self, al_id):
        query = "select * from item_profile where al_id=" +  str(al_id)
        al_token = self.cursor.execute(query).fetchall()
        # 리스트 타입 반환  :  0번째는 u_id
        df = pd.DataFrame(data = {'tokens':al_token[0][1:]}).replace('', 0)
        df.index = token_list
        return df


    # 사용자 별 알콜에 대한 토큰 선호도 순위
    def get_token_rank(self):
        al_token = self.select_al_token(self.al_id)
        user_token = self.select_user_token(self.c_id)

        al_tokens = al_token.replace(0, np.NAN).dropna().index.to_list()
        user_token_score = user_token.replace(0, np.NaN).dropna()
        user_token_score.reset_index(inplace=True)
        token_seq = user_token_score[user_token_score['index'].isin(al_tokens)].sort_values(by = 'tokens', ascending=False)
        token_rank = token_seq['index'].values.tolist()
        return token_rank
    

class item_list:
    def __init__(self, cid):
        # MAC용
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        # Window용
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.c_id = cid

    def get_top15(self):
        rankings = pd.read_csv('flask-server/db/db_csv_data/ranking_new.csv')
        rankings_t = rankings.reset_index().drop(columns='index').T
        rankings_t.reset_index(inplace=True)

        rank_df = pd.DataFrame()
        # 1~15등 rank 칼럼 생성
        rank_df['rank'] = np.arange(1,16)
        # merge를 위해 인덱스 리셋
        rank_df.index = np.arange(1, 16)
        # 전통주 이름이 안맞아서 top 15를 뽑지 못하는 것 같음,, 이름을 맞춰야겠네
        rank_df['al_name'] = rankings_t[self.c_id][1:16]
        al_name_tuple = tuple(rank_df['al_name'].values.tolist())

        # top15에 해당하는 알콜 이름으로 쿼리 날림
        query = "select al_name, al_id, img_link, category, degree from item_info where al_name in " +  str(al_name_tuple)
        al_token = self.cursor.execute(query).fetchall()
        al_df = pd.DataFrame(al_token, columns=['al_name', 'al_id', 'img_link', 'category', 'degree'])

        rank_df = pd.merge(rank_df, al_df, on='al_name', how='inner')
        rank_df['c_id'] = self.c_id

        return rank_df

    def get_top15_json(self):
        rank_df = self.get_top15()
        return rank_df.T.to_json(force_ascii=False)

    def get_all_alcohols_df(self):
        query = "select al_name, al_id, img_link, category, degree from item_info"
        al_token = self.cursor.execute(query).fetchall()
        al_df = pd.DataFrame(al_token, columns=['al_name', 'al_id', 'img_link', 'category', 'degree'])        
        al_df = al_df.sample(frac=1)
        return al_df

    def get_alcohols_df_by_category(self, category):
        query = "select al_name, al_id, img_link, category, degree from item_info where category = '" + category + "'"
        al_token = self.cursor.execute(query).fetchall()
        al_df = pd.DataFrame(al_token, columns=['al_name', 'al_id', 'img_link', 'category', 'degree'])        
        al_df = al_df.sample(frac=1)
        return al_df
    
    def get_alcohols_json(self, category):
        if(category == None):
            # 지정된 카테고리 없으면 전체 데이터 출력 
            al_df = self.get_all_alcohols_df()
        else:
            al_df = self.get_alcohols_df_by_category(category)
        return al_df.T.to_json(force_ascii=False)



class user_sign:
    def __init__(self):
        # MAC용
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        # Window용
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()

    def sign_in(self, user_sign_id, user_sign_pw):
        query = "select * from users where user_sign_id='" + user_sign_id + "' and user_sign_pw = '" + user_sign_pw + "'"
        result = self.cursor.execute(query).fetchall()
        
        if len(result) == 0:
            return 'False'
        else:
            self.c_id = result[0][0]
            self.c_name = result[0][3]
            return (self.c_id, self.c_name)


    def duplicate_id_check(self, c_id):
        query = "select count(*) from users where user_sign_id='" + c_id + "'"
        result = self.cursor.execute(query).fetchall()

        if result[0][0] == 0:
            return 1
        else:
            return 0


    def duplicate_name_check(self, c_name):
        query = "select count(*) from users where u_name='" + c_name + "'"
        result = self.cursor.execute(query).fetchall()

        if result[0][0] == 0:
            return 1
        else:
            return 0

    
    def sign_up(self, user_sign_id, user_sign_pw, u_name):
        query01 = 'select u_id from users order by rowid desc limit 1'
        last_u_id = self.cursor.execute(query01).fetchall()[0][0]
        
        query02 = "insert into users (u_id, user_sign_id, user_sign_pw, u_name) values (?, ?, ?, ?)"
        data = (last_u_id + 1, user_sign_id, user_sign_pw, u_name)
        try:
            self.cursor.execute(query02, data)
            self.conn.commit()
            return 1
        except:
            return 0


# detail 페이지에서 구매하기 버튼 누르면, but_info에 c_id, al_id, datetime 저장됨
# 현재시간 - datetime > 14days  =>  detail 페이지에 리뷰 남기기 버튼 존재 (선택)
# mypage  =>  구매한 아이템 리스트 나열  =>  14일 이전이면, 리뷰 남기기 버튼 o
# 구매하기 버튼 누르면 buy_info에 글이 남겨짐
class buy:
    def __init__(self, c_id):
        self.c_id = c_id
        self.now = datetime.now()

        # MAC용
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        # Window용
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()


    # 사용자 - 아이템 별 리뷰 남길 수 있는지 확인
    # 16번 사람은 133번을 두 번 마심,,
    def review_able(self, time):
        time = datetime.strptime(time, "%Y.%m.%d")
        print(time)
        if ((self.now - time).days < 15):
            return 1
        else:
            return 0

    # mypage에서 사용
    # 사용자 별 구매한 아이템 나열  :  Dataframe 반환  :  json으로 변환해야함
    def purchase_items(self):
        query = "select b.u_id, i.al_id, i.al_name, b.datetime from buy_info b, item_info i where b.al_id = i.al_id and b.u_id = " + str(self.c_id)
        result = pd.DataFrame(self.cursor.execute(query).fetchall(), columns = ['c_id', 'al_id', 'al_name', 'date'])

        # 1이면 리뷰 쓰라는 버튼 나오고, 0이면 안나옴
        result['review_O'] = result['date'].apply(self.review_able)
        return result.T.to_json(force_ascii=False)


    # detail에서 사용  :  구매한지 15일 미만이면 리뷰 버튼 생성
    # 버튼 생성해야하면 1, 아니면 0 반환
    def review_button(self, al_id):
        query = '''select b.u_id, i.al_id, i.al_name, b.datetime 
                from buy_info b, item_info i 
                where b.al_id = i.al_id and b.u_id =''' + str(self.c_id) + ' and i.al_id= ' + str(al_id) + ' order by datetime desc'
        result = self.cursor.execute(query).fetchone()
        time = datetime.strptime(result[3], "%Y.%m.%d")

        if (self.now - time).days < 15:
            return 1
        else:
            return 0


    # 리뷰 작성 버튼 누르고, 별점 눌렀을 때 리뷰 점수 저장됨
    # 리뷰 점수(<=5) 필요함
    # 저장되면 return 1 else return 0
    def write_review(self, al_id, score):
        query = "select b.u_id, b.al_id, u.u_name, i.al_name from buy_info b, users u, item_info i where b.u_id = u.u_id and b.al_id = i.al_id and u.u_id = ? and i.al_id = ?  order by b.datetime desc"
        data = (self.c_id, al_id)
        # c_id, al_id, u_name, al_name
        result = self.cursor.execute(query, data).fetchone()

        date = str(self.now.year) + '.' + str(self.now.month) + '.' + str(self.now.day) 
        query = "insert into reviews values(?, ?, ?, ?, ?, ?)"
        data = (result[0], result[3], result[1], result[2], score, date)
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            return 1
        except:
            return 0




    # 구매 버튼 누르면 buy_info에 넣음
    # 넣는 것 성공하면 return 1 else 0
    def add_purchase(self, al_id):
        date = str(self.now.year) + '.' + str(self.now.month) + '.' + str(self.now.day) 
        query = "insert into buy_info values(?, ?, ?)"
        data = (al_id, self.c_id, date)
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            return 1
        except:
            return 0




a = buy(16)
a.write_review(133, 23)