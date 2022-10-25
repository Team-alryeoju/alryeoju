from lib2to3.pgen2 import token
import pandas as pd
import numpy as np
import sqlite3
import pprint

token_list = ['감칠맛', '걸쭉함', '견과류_땅콩_잣향', '고소함', '곡물_옥수수_보리', '기타_커피_캐러멜_토란',
       '깔끔', '꿀맛_당류', '누룩', '다양', '단맛', '독특', '드라이', '레몬_유자류_감귤류_자몽',
       '매실류_파인애플', '바나나_망고_멜론', '바닐라_국화_매화_연꽃_유채꽃_꽃향', '베리류_딸기', '사과_배_감',
       '스모키한', '신맛', '여운', '열대과일', '오디_복분자', '오미자류', '음료', '인삼_생강강황_약재',
       '자두_복숭아_체리', '잔잔한', '조화', '진득', '청_포도', '청량', '탄닌감', '탄산', '풀내음_나무_볏짚',
       '허브_시트러스', '화끈함']

# 디테일 페이지 만들기
class detail_info:
    def __init__(self, cid, alid):
        self.conn = sqlite3.connect('./db/alryeoju.db')
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
        self.conn = sqlite3.connect('./db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.c_id = cid

    def get_top15(self):

        rankings = pd.read_csv('./db/db_csv_data/ranking_new.csv')
        rankings_t = rankings.reset_index().drop(columns='index').T
        rankings_t.reset_index(inplace=True)

        rank_df = pd.DataFrame()
        # 1~15등 rank 칼럼 생성
        rank_df['rank'] = np.arange(1,16)
        # merge를 위해 인덱스 리셋
        rank_df.index = np.arange(1, 16)
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
