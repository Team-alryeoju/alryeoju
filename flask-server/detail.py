# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

token_list = ['가득한', '가벼운', '가볍게', '가볍고', '간단한', '간장', '감압식', '감압식 증류', '감칠맛', '감칠맛을', '감칠맛이', '강렬한', '강하게', '강하지',
 '강한', '거친', '고구마', '고구마의', '고기', '고소', '고소하고', '고소한', '고소함과', '고운달', '곡물', '곡물의', '과실', '과실의',
  '과일', '구수하면서도', '구수한', '국물', '궁합을', '궁합이', '기름진', '기름진 깔끔하게', '기분', '깊은', '깊은 풍미를', '깔끔하게', '깔끔하고', '깔끔한',
 '냉장', '냉장고에', '냉장고에서', '높고', '높은', '높은 도수를', '높은 도수와', '누룩', '누룩으로', '누룩을', '누룩의', '느끼한', '느끼함을',
 '다양한', '다채로운', '단맛', '단맛과', '단맛과 산미가', '단맛으로', '단맛은', '단맛을', '단맛이', '달달한', '달지', '달짝지근한', '달콤', '달콤하게',
 '달콤하고', '달콤하면서도', '달콤한', '달콤함', '달콤함과', '달콤함은', '달콤함이', '담백하고', '담백한', '도수가', '도수를', '도수에', '도수와',
 '독특한', '독특한 풍미를', '동백꽃', '드라이한', '디저트류와', '디저트와', '딸기', '떫은', '레드', '레몬', '로제', '막걸리', '막걸리는', '막걸리를',
 '막걸리의', '맑고', '맑은', '매실', '매실의', '매운', '매운맛을', '매콤한', '매콤한 양념이', '무화과', '묵직한', '물과', '물을', '물처럼', '바나나',
 '바디감과', '바디감을', '바디감이', '발효', '발효를', '발효시켜', '발효와', '발효와 숙성을', '발효한', '배가', '베리류의', '복분자의', '복숭아', '복합적으로',
 '복합적인', '부드러운', '부드러운 단맛', '부드럽게', '부드럽고', '부드럽고 깔끔한', '붉은', '사과', '사과로', '사과를', '사과의', '사이다', '산뜻하게',
 '산뜻한', '산미', '산미가', '산미는', '산미를', '산미와', '상온에', '상온에서', '상쾌한', '상큼한', '새콤달콤한', '새콤달콤함이', '새콤한', '생선회',
 '소주', '소주는', '소주를', '소주와', '소주의', '수제', '숙성', '숙성을', '숙성한', '스위트', '스트레이트로', '스파클링', '시원하게', '시원한', '시트러스',
 '식욕을', '식전주로', '신맛이', '신선한', '싱그러운', '싱그럽게', '쌀과', '쌀로', '쌀을', '쌀의', '쏘는', '씁쓸한', '씁쓸함이', '아니라', '안주', '안주류와',
 '안주와', '알싸한', '알코올', '압력을', '압력을 증류하는', '애플', '약주', '약주입니다', '양념', '양념된', '양념이', '양념이 강한', '얼음', '얼음을',
 '여운을', '여운이', '오미자', '오미자를', '오미자의', '오크', '오크통', '온더락으로', '온도가', '온도에', '온도에서', '올라오는데요', '와인', '와인은',
 '와인을', '와인의', '와인이에요', '와인인데요', '와인입니다', '원액을', '원주를', '유기농', '육류', '육류나', '육류와', '은은하게', '은은한', '은은한 단맛과',
 '음식보단', '자극하는', '자두', '자연', '작열감', '작열감과', '작열감도', '작열감을', '작열감이', '저온', '저온 숙성을', '저온에서', '적은', '적절한',
 '전통주', '조화로운', '주스', '주스처럼', '중후한', '증류', '증류를', '증류식', '증류주', '증류주를', '증류하는', '증류하는 감압식', '증류하여', '증류한',
 '진득한', '진한', '질감을', '집에서', '짙은', '짭조름한', '짭짤한', '차가운', '차갑게', '찹쌀과', '첨가물', '청량감', '청포도', '치즈', '친구들과', '크라테',
 '탁주', '탁주는', '탁주의', '탄산', '탄산과', '탄산이', '텁텁한', '투명한', '튀는', '특별한', '특유의', '특징이', '편안하게', '포도', '포도로', '포도를',
 '포도의', '풍미', '풍미 짙은', '풍미가', '풍미가 짙은', '풍미까지', '풍미는', '풍미를', '풍미와', '풍부하게', '풍부한', '해산물', '향긋한', '화이트', '효모를',
 'degree']

# 디테일 페이지 만들기
class detail_info:
    def __init__(self, alid, cid = -1):
        #Mac용
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        # window  :  mac도 가능한가 확인 좀,,
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.c_id = cid
        self.al_id = alid
        
    # 사용자 별 토큰 값 가져오기
    def select_user_token(self):
        query = "select * from user_profile where u_id=" +  str(self.c_id)
        user_token = self.cursor.execute(query).fetchall()
        # 리스트 타입 반환
        df = pd.DataFrame(data = {'tokens':user_token[0][2:-1]}).replace('', 0)
        df.index = token_list[:-1]
        return df
    
    # 아이템 별 토큰 값 가져오기
    def select_al_token(self):
        query = "select * from item_profile where al_id=" +  str(self.al_id)
        al_token = self.cursor.execute(query).fetchall()
        
        # 리스트 타입 반환  :  0번째는 u_id
        df = pd.DataFrame(data = {'tokens':al_token[0][3:]}).replace('', 0)
        df.index = token_list[:-1]
        return df


    # 사용자 별 알콜에 대한 토큰 선호도 순위
    def get_token_rank(self):
        # 로그인 안했을 때는 c_id가 None
        if self.c_id != -1:
            al_token = self.select_al_token()
            user_token = self.select_user_token()

            al_tokens = al_token.replace(0, np.NAN).dropna().index.to_list()
            user_token_score = user_token.replace(0, np.NaN).dropna()
            user_token_score.reset_index(inplace=True)
            token_seq = user_token_score[user_token_score['index'].isin(al_tokens)].sort_values(by = 'tokens', ascending=False)
            token_rank = token_seq['index'].values.tolist()
            token_rank = token_rank + list(set(al_tokens) - set(token_rank))
        else:
            al_token = self.select_al_token()
            token_rank = al_token.replace(0, np.NAN).dropna().index.to_list()

        return token_rank
    

    # 아이템 평균 점수
    def get_score(self, al_id):
        query = "select al_id, score from reviews where al_id = " + str(al_id)
        scores = self.cursor.execute(query).fetchall()

        c = pd.DataFrame(data = scores, columns = ['al_id', 'scores'])
        if c.empty:
            return 0
        else:
            return c.mean().scores

    
    # 알콜 정보를 넘기자
    def al_info_df(self):
        query = """select al_id, al_name, category, price, degree, img_link
                from item_info where al_id = ?"""
        data = (self.al_id,)
        result = self.cursor.execute(query, data).fetchall()

        columns_ = ['al_id', 'al_name', 'category', 'price', 'degree', 'img_link']
        
        al_data = pd.DataFrame(data = result, columns = columns_, index=['al_data'])
        return al_data 


        al_data['score'] = al_data.al_id.apply(self.get_score)
        
        return al_data.T.to_dict()
    
    
    # 알콜 토큰 랭크와 정보 취합하기
    def detail_page(self, page):        
        # page == 2  :  /recomm => top15함수들에서 호출  =>  score 계산 안함
        token_rank = self.get_token_rank()
        al_data = self.al_info_df()

        # page == 1  :  /detail에서 호출
        if page == 1:
            al_data['score'] = al_data.al_id.apply(self.get_score)
            al_data = al_data.T.to_dict()
            al_data['token_rank'] = token_rank
            return al_data
        if page == 2:
            return al_data.T.to_dict()




# 디테일 페이지 하단부분  :  리뷰 읽기
class reviews:
    def __init__(self, al_id):
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.al_id = al_id
    
    def get_reviews(self):
        query = "select u_name, al_name, review, score, datetime from reviews where al_id=" + str(self.al_id)
        reviews_lst = self.cursor.execute(query).fetchall()

        reviews_df = pd.DataFrame(data = reviews_lst, columns=['u_name', 'al_name', 'review', 'score', 'datetime']).sort_values(by='datetime', ascending=False)
        
        return reviews_df.T.to_dict()
    



survey = dict()
survey['1a'] = ['깊은', '깊은 풍미를','씁쓸한','씁쓸함이', '풍미', '풍미 짙은', '풍미가', '풍미가 짙은','풍미까지', '풍미는', '풍미를', '풍미와', '진득한', '진한']
survey['1b'] = ['고소','고소하고','고소한', '고소함과', '구수하면서도', '구수한','부드러운', '부드러운 단맛', '부드럽게', '부드럽고', '부드럽고 깔끔한']
survey['1c'] = ['산미', '산미가','산미는', '산미를', '산미와', '신맛이', '여운을', '여운이', '은은하게', '은은한', '은은한 단맛과']
survey['2a'] = [ '가벼운', '가볍게', '가볍고', '산뜻하게', '산뜻한', '상쾌한','시트러스', '싱그러운', '싱그럽게']
survey['2b'] = [ '묵직한', '바디감과', '바디감을', '바디감이','오크','오크통', '자연','중후한']
survey['3a'] = ['사이다','시원하게','시원한', '스파클링', '쏘는', '자극하는', '차가운','차갑게', '청량감', '탄산', '탄산과','탄산이']
survey['3b'] = ['기름진','기름진 깔끔하게','깔끔하게', '깔끔하고', '깔끔한', '느끼한', '느끼함을','부드럽고 깔끔한','여운을', '여운이', '은은하게', '은은한', '은은한 단맛과']
survey['4a'] = [ '단맛', '단맛과', '단맛과 산미가', '단맛으로','단맛은', '단맛을', '단맛이', '달달한', '달지', '달짝지근한', '달콤', '달콤하게', '달콤하고', '달콤하면서도', '달콤한', '달콤함','달콤함과', '달콤함은', '달콤함이', '부드러운', '부드러운 단맛', '부드럽게', '부드럽고', '부드럽고 깔끔한', '스위트']
survey['4b'] = [ '깔끔하게', '깔끔하고', '깔끔한','부드럽고 깔끔한','시원하게', '시원한', '차가운', '차갑게']
survey['4c'] = [ '단맛','단맛과','단맛과 산미가','단맛으로','단맛은', '단맛을', '단맛이', '달달한', '달지', '달짝지근한', '달콤', '달콤하게', '달콤하고', '달콤하면서도','달콤한', '달콤함', '달콤함과', '달콤함은', '달콤함이', '산미', '산미가', '산미는', '산미를','산미와', '상큼한', '새콤달콤한', '새콤달콤함이','새콤한', '신맛이']
survey['5a'] = [ '국물','매운', '매운맛을', '매콤한', '매콤한 양념이', '안주', '안주류와', '안주와', '양념', '양념된', '양념이', '양념이 강한', '짭조름한', '짭짤한', '해산물']
survey['5b'] = [ '국물','깔끔하게', '깔끔하고', '깔끔한', '담백하고','담백한', '해산물', '간장', '기름진', '기름진 깔끔하게', '안주','안주류와','안주와']
survey['5c'] = [ '해산물', '안주', '안주류와','안주와', '생선회', '신선한','자연']


class item_list:
    def __init__(self, cid = -1):
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()
        self.c_id = cid
    

    # item_profile 읽어서 df로 만들기
    def item_profile_df(self):
        query = "select * from item_profile"
        al_profile = self.cursor.execute(query).fetchall()
        
        df = pd.DataFrame(data = al_profile, columns = ['al_id', 'al_name', 'degree'] + token_list[:-1])
        return df


    # 아이템 단일 행 읽기
    def an_item_profile_df(self, al_id):
        query = "select * from item_profile where al_id = " + str(al_id)
        al_row = self.cursor.execute(query).fetchall()

        df = pd.DataFrame(data = al_row, columns = ['al_id', 'al_name', 'degree'] + token_list[:-1])
        return df


    # 사용자 프로파일에서 특정 사용자 정보 df로 읽기
    def c_user_profile(self):
        query = "select * from user_profile where u_id = " + str(self.c_id)
        user = self.cursor.execute(query).fetchall()

        df = pd.DataFrame(data = user, columns=['u_id', 'u_name'] + token_list)
        return df


    # 비슷한 술 6개의 아이디
    def sim_items_6_id(self, al_id):
        al_row= self.an_item_profile_df(al_id)[token_list]
        item_profile = self.item_profile_df()
        item_matrix = item_profile[token_list]

        similarity = cosine_similarity(al_row, item_matrix) 
        # 사용자와 아이템들 간의 유사도를 내림차순으로 정렬하여 상위 15개의 인덱스 추출
        top_15_idx = np.argsort(similarity[0])[::-1][1:7]
        # 상위 15개의 아이템 아이디
        top_15_ids = item_profile.loc[top_15_idx].al_id.to_list()

        return top_15_ids

    # 비슷한 술 6개 아이템 데이터 반환
    def get_sim_6(self, al_id):
        sim6_ids = self.sim_items_6_id(al_id)

        # 상위 순서대로 추출해야해서 for문 돌려야함
        result = dict()
        for idx, id in enumerate(sim6_ids):
            detail_data = detail_info(alid=id)
            result[idx] = detail_data.detail_page(page=2)['al_data']

        return result


    # 상위 15개의 아이템 아이디 반환
    def get_top15_id(self):
        user_row = self.c_user_profile()[token_list]
        item_profile = self.item_profile_df()
        item_matrix = item_profile[token_list]

        similarity = cosine_similarity(user_row, item_matrix) 
        # 사용자와 아이템들 간의 유사도를 내림차순으로 정렬하여 상위 15개의 인덱스 추출
        top_15_idx = np.argsort(similarity[0])[::-1][:15]
        # 상위 15개의 아이템 아이디
        top_15_ids = item_profile.loc[top_15_idx].al_id.to_list()

        return top_15_ids


    # top15개의 아이템 데이터 반환
    def get_top15(self):
        query = "select cnt from users where u_id = " + str(self.c_id)
        cnt = self.cursor.execute(query).fetchone()[0]
        if cnt == 0:
            return self.best_15()
        else:
            top15_ids = self.get_top15_id()

            # 상위 순서대로 추출해야해서 for문 돌려야함
            result = dict()
            for idx, id in enumerate(top15_ids):
                detail_data = detail_info(alid=id)
                result[idx] = detail_data.detail_page(page=2)['al_data']

            return result


    # c_id = -1일 때 베스트 아이템(리뷰 점수 높은거,,)
    def best_15(self):
        query = "select al_id, score from reviews"
        al_scores = self.cursor.execute(query).fetchall()
        al_scores_df = pd.DataFrame(al_scores, columns=['al_id', 'score'])
        best15_al_id = al_scores_df.pivot_table(index='al_id', values='score', aggfunc='mean').sort_values(by='score', ascending=False).reset_index()['al_id'][:15].to_list()
        
        # 상위 순서대로 추출해야해서 for문 돌려야함
        result = dict()
        for idx, id in enumerate(best15_al_id):
            detail_data = detail_info(alid=id)
            result[idx] = detail_data.detail_page(page=2)['al_data']

        return result


    def get_all_alcohols_df(self):
        query = "select al_id, al_name, category, price, degree, img_link from item_info"
        al_token = self.cursor.execute(query).fetchall()
        al_df = pd.DataFrame(al_token, columns=['al_id', 'al_name', 'category', 'price', 'degree', 'img_link'])        
        al_df = al_df.sample(frac=1)
        return al_df

    def get_alcohols_df_by_category(self, category):
        query = "select al_id, al_name, category, price, degree, img_link from item_info where category = '" + category + "'"
        al_token = self.cursor.execute(query).fetchall()
        al_df = pd.DataFrame(al_token, columns=['al_id', 'al_name', 'category', 'price', 'degree', 'img_link'])        
        al_df = al_df.sample(frac=1)
        return al_df
    
    def get_alcohols_json(self, category):
        if(category == None):
            # 지정된 카테고리 없으면 전체 데이터 출력 
            al_df = self.get_all_alcohols_df()
        else:
            al_df = self.get_alcohols_df_by_category(category)
        return al_df.T.to_json(force_ascii=False)


    def survey(self, ans1, ans2, ans3, ans4, ans5):
        include = list(set(survey[ans1] + survey[ans2] + survey[ans3] + survey[ans4] + survey[ans5]))
        dic = dict()
        for t in token_list[:-1]:
            if t in include:
                dic[t] = [1]
            else:
                dic[t] = [0]

        ans = pd.DataFrame(dic)

        a = item_list()
        items = a.item_profile_df()
        item_profile = items[token_list[:-1]]

        similarity = cosine_similarity(ans, item_profile) 
        top_6_idx = np.argsort(similarity[0])[::-1][:6]
        top_6_ids = items.loc[top_6_idx].al_id.to_list()


        result = dict()
        for idx, id in enumerate(top_6_ids):
            detail_data = detail_info(alid=id)
            result[idx] = detail_data.detail_page(page=2)['al_data']

        return result





class user_sign:
    def __init__(self):
        # self.conn = sqlite3.connect('./db/alryeoju.db')
        self.conn = sqlite3.connect('flask-server/db/alryeoju.db')
        self.cursor = self.conn.cursor()

    def sign_in(self, user_sign_id, user_sign_pw):
        query = "select * from users where user_sign_id='" + user_sign_id + "' and user_sign_pw = '" + user_sign_pw + "'"
        result = self.cursor.execute(query).fetchall()
        
        if len(result) == 0:
            return False
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
        
        # users 테이블에 행 생성
        query02 = 'insert into users (u_id, user_sign_id, user_sign_pw, u_name, cnt) values (?, ?, ?, ?, ?)'
        data02 = (last_u_id + 1, user_sign_id, user_sign_pw, u_name, 0)

        # user_profile 테이블에 행 생성
        query03 =  'insert into user_profile (u_id , u_name ,가득한 ,가벼운 ,가볍게 ,가볍고 ,간단한 ,간장 ,감압식 ,감압식_증류 ,감칠맛 ,감칠맛을 ,감칠맛이 ,강렬한 ,강하게 ,강하지 ,강한 ,거친 ,고구마 ,고구마의 ,고기 ,고소 ,고소하고 ,고소한 ,고소함과 ,고운달 ,곡물 ,곡물의 ,과실 ,과실의 ,과일 ,구수하면서도 ,구수한 ,국물 ,궁합을 ,궁합이 ,기름진 ,기름진_깔끔하게 ,기분 ,깊은 ,깊은_풍미를 ,깔끔하게 ,깔끔하고 ,깔끔한 ,냉장 ,냉장고에 ,냉장고에서 ,높고 ,높은 ,높은_도수를 ,높은_도수와 ,누룩 ,누룩으로 ,누룩을 ,누룩의 ,느끼한 ,느끼함을 ,다양한 ,다채로운 ,단맛 ,단맛과 ,단맛과_산미가 ,단맛으로 ,단맛은 ,단맛을 ,단맛이 ,달달한 ,달지 ,달짝지근한 ,달콤 ,달콤하게 ,달콤하고,달콤하면서도 ,달콤한 ,달콤함 ,달콤함과 ,달콤함은 ,달콤함이 ,담백하고 ,담백한 ,도수가 ,도수를 ,도수에 ,도수와 ,독특한 ,독특한_풍미를 ,동백꽃 ,드라이한 ,디저트류와 ,디저트와 ,딸기 ,떫은 ,레드 ,레몬 ,로제 ,막걸리 ,막걸리는 ,막걸리를 ,막걸리의 ,맑고 ,맑은 ,매실 ,매실의 ,매운 ,매운맛을 ,매콤한 ,매콤한_양념이 ,무화과 ,묵직한 ,물과 ,물을 ,물처럼 ,바나나 ,바디감과 ,바디감을 ,바디감이,발효 ,발효를 ,발효시켜 ,발효와 ,발효와_숙성을 ,발효한 ,배가 ,베리류의 ,복분자의 ,복숭아 ,복합적으로 ,복합적인 ,부드러운 ,부드러운_단맛 ,부드럽게 ,부드럽고 ,부드럽고_깔끔한 ,붉은 ,사과 ,사과로 ,사과를 ,사과의 ,사이다 ,산뜻하게 ,산뜻한 ,산미 ,산미가 ,산미는 ,산미를 ,산미와 ,상온에 ,상온에서 ,상쾌한 ,상큼한 ,새콤달콤한 ,새콤달콤함이 ,새콤한 ,생선회 ,소주 ,소주는 ,소주를 ,소주와 ,소주의 ,수제 ,숙성 ,숙성을 ,숙성한 ,스위트 ,스트레이트로 ,스파클링 ,시원하게 ,시원한 ,시트러스 ,식욕을 ,식전주로 ,신맛이 ,신선한 ,싱그러운 ,싱그럽게 ,쌀과 ,쌀로 ,쌀을 ,쌀의 ,쏘는 ,씁쓸한 ,씁쓸함이 ,아니라 ,안주 ,안주류와 ,안주와 ,알싸한 ,알코올 ,압력을 ,압력을_증류하는 ,애플 ,약주 ,약주입니다 ,양념 ,양념된 ,양념이 ,양념이_강한 ,얼음 ,얼음을 ,여운을 ,여운이 ,오미자 ,오미자를 ,오미자의 ,오크 ,오크통 ,온더락으로 ,온도가 ,온도에 ,온도에서 ,올라오는데요 ,와인 ,와인은 ,와인을 ,와인의 ,와인이에요 ,와인인데요 ,와인입니다 ,원액을 ,원주를 ,유기농 ,육류 ,육류나 ,육류와 ,은은하게 ,은은한 ,은은한_단맛과 ,음식보단 ,자극하는 ,자두 ,자연 ,작열감 ,작열감과 ,작열감도 ,작열감을 ,작열감이 ,저온 ,저온_숙성을 ,저온에서 ,적은 ,적절한 ,전통주 ,조화로운 ,주스 ,주스처럼 ,중후한 ,증류 ,증류를 ,증류식 ,증류주 ,증류주를 ,증류하는 ,증류하는_감압식 ,증류하여 ,증류한 ,진득한 ,진한 ,질감을 ,집에서 ,짙은 ,짭조름한 ,짭짤한 ,차가운 ,차갑게 ,찹쌀과 ,첨가물 ,청량감 ,청포도 ,치즈 ,친구들과 ,크라테 ,탁주 ,탁주는 ,탁주의 ,탄산 ,탄산과 ,탄산이 ,텁텁한 ,투명한 ,튀는 ,특별한 ,특유의 ,특징이 ,편안하게 ,포도 ,포도로 ,포도를 ,포도의 ,풍미 ,풍미_짙은,풍미가 ,풍미가_짙은 ,풍미까지 ,풍미는 ,풍미를 ,풍미와 ,풍부하게 ,풍부한 ,해산물 ,향긋한 ,화이트 ,효모를 ,degree) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        data03 = (last_u_id + 1, user_sign_id, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        try:            
            self.cursor.execute(query02, data02)
            self.cursor.execute(query03, data03)
            self.conn.commit()
            return 1
        except:
            return 0




# detail 페이지에서 구매하기 버튼 누르면, buy_info에 c_id, al_id, datetime 저장됨
# 현재시간 - datetime > 14days  =>  detail 페이지에 리뷰 남기기 버튼 존재 (선택)
# mypage  =>  구매한 아이템 리스트 나열  =>  14일 이전이면, 리뷰 남기기 버튼 o
# 구매하기 버튼 누르면 buy_info에 글이 남겨짐
# 밑의 함수에서,, apply때 쓸려고 평균내기 함수 만듦,,
def mean(x, cnt):
    if x[0] == 0:
        return x[1]
    elif x[1] == 0:
        return x[0]
    else:
        return (x[0]*(cnt-1) + x[1])/cnt

class buy:
    def __init__(self, c_id):
        self.c_id = c_id
        self.now = datetime.now()

        # self.conn = sqlite3.connect('./db/alryeoju.db')
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
    def write_review(self, c_name, al_id, al_name, review, score):
        date = str(self.now.year) + '.' + str(self.now.month) + '.' + str(self.now.day) 
        query = "insert into reviews values(?, ?, ?, ?, ?, ?, ?)"
        data = (self.c_id, c_name, al_id, al_name, score, review, date)
        try:
            self.cursor.execute(query, data)
            self.conn.commit()

            self.user_profile_update(al_id)
            return 1
        except:
            return 0



    # 리뷰 작성시 user_profile 업데이트 하기
    def user_profile_update(self, al_id):
        query = "select p.*, u.cnt from user_profile p, users u where p.u_id = u.u_id and u.u_id = " + str(self.c_id)
        user_row = self.cursor.execute(query).fetchall()
        user_row = pd.DataFrame(data = user_row, columns=['u_id', 'u_name'] + token_list + ['cnt'])
        # 총 구매 개수
        cnt = user_row.loc[0, 'cnt'] + 1
        user_p = user_row[token_list].T
        
        query = "select * from item_profile where al_id = " + str(al_id)
        al_row = self.cursor.execute(query).fetchall()
        al_row = pd.DataFrame(data = al_row, columns = ['al_id', 'al_name', 'degree'] + token_list[:-1])
        al_p = al_row[token_list].T
        
        
        # 사용자 토큰과 아이템 토큰 반영
        a = pd.DataFrame(user_p).rename(columns={0:'df1'})
        a['df2'] = al_p
        # 과거 데이터의 비중 : 80%, 현재 아이템의 비중 : 20%
        a['result'] = a.apply(mean, args=(5, ), axis=1)
        result = a.T.loc[['result']]
        result['u_id'] = user_row.loc[0, 'u_id']
        result['u_name'] = user_row.loc[0, 'u_name']
        result['cnt'] = cnt
        result = result[['u_id', 'u_name'] + token_list]

        # 행 삭제 후 재 삽입
        query = "delete from user_profile where u_id = " + str(self.c_id)
        query02 =  'insert into user_profile (u_id , u_name ,가득한 ,가벼운 ,가볍게 ,가볍고 ,간단한 ,간장 ,감압식 ,감압식_증류 ,감칠맛 ,감칠맛을 ,감칠맛이 ,강렬한 ,강하게 ,강하지 ,강한 ,거친 ,고구마 ,고구마의 ,고기 ,고소 ,고소하고 ,고소한 ,고소함과 ,고운달 ,곡물 ,곡물의 ,과실 ,과실의 ,과일 ,구수하면서도 ,구수한 ,국물 ,궁합을 ,궁합이 ,기름진 ,기름진_깔끔하게 ,기분 ,깊은 ,깊은_풍미를 ,깔끔하게 ,깔끔하고 ,깔끔한 ,냉장 ,냉장고에 ,냉장고에서 ,높고 ,높은 ,높은_도수를 ,높은_도수와 ,누룩 ,누룩으로 ,누룩을 ,누룩의 ,느끼한 ,느끼함을 ,다양한 ,다채로운 ,단맛 ,단맛과 ,단맛과_산미가 ,단맛으로 ,단맛은 ,단맛을 ,단맛이 ,달달한 ,달지 ,달짝지근한 ,달콤 ,달콤하게 ,달콤하고,달콤하면서도 ,달콤한 ,달콤함 ,달콤함과 ,달콤함은 ,달콤함이 ,담백하고 ,담백한 ,도수가 ,도수를 ,도수에 ,도수와 ,독특한 ,독특한_풍미를 ,동백꽃 ,드라이한 ,디저트류와 ,디저트와 ,딸기 ,떫은 ,레드 ,레몬 ,로제 ,막걸리 ,막걸리는 ,막걸리를 ,막걸리의 ,맑고 ,맑은 ,매실 ,매실의 ,매운 ,매운맛을 ,매콤한 ,매콤한_양념이 ,무화과 ,묵직한 ,물과 ,물을 ,물처럼 ,바나나 ,바디감과 ,바디감을 ,바디감이,발효 ,발효를 ,발효시켜 ,발효와 ,발효와_숙성을 ,발효한 ,배가 ,베리류의 ,복분자의 ,복숭아 ,복합적으로 ,복합적인 ,부드러운 ,부드러운_단맛 ,부드럽게 ,부드럽고 ,부드럽고_깔끔한 ,붉은 ,사과 ,사과로 ,사과를 ,사과의 ,사이다 ,산뜻하게 ,산뜻한 ,산미 ,산미가 ,산미는 ,산미를 ,산미와 ,상온에 ,상온에서 ,상쾌한 ,상큼한 ,새콤달콤한 ,새콤달콤함이 ,새콤한 ,생선회 ,소주 ,소주는 ,소주를 ,소주와 ,소주의 ,수제 ,숙성 ,숙성을 ,숙성한 ,스위트 ,스트레이트로 ,스파클링 ,시원하게 ,시원한 ,시트러스 ,식욕을 ,식전주로 ,신맛이 ,신선한 ,싱그러운 ,싱그럽게 ,쌀과 ,쌀로 ,쌀을 ,쌀의 ,쏘는 ,씁쓸한 ,씁쓸함이 ,아니라 ,안주 ,안주류와 ,안주와 ,알싸한 ,알코올 ,압력을 ,압력을_증류하는 ,애플 ,약주 ,약주입니다 ,양념 ,양념된 ,양념이 ,양념이_강한 ,얼음 ,얼음을 ,여운을 ,여운이 ,오미자 ,오미자를 ,오미자의 ,오크 ,오크통 ,온더락으로 ,온도가 ,온도에 ,온도에서 ,올라오는데요 ,와인 ,와인은 ,와인을 ,와인의 ,와인이에요 ,와인인데요 ,와인입니다 ,원액을 ,원주를 ,유기농 ,육류 ,육류나 ,육류와 ,은은하게 ,은은한 ,은은한_단맛과 ,음식보단 ,자극하는 ,자두 ,자연 ,작열감 ,작열감과 ,작열감도 ,작열감을 ,작열감이 ,저온 ,저온_숙성을 ,저온에서 ,적은 ,적절한 ,전통주 ,조화로운 ,주스 ,주스처럼 ,중후한 ,증류 ,증류를 ,증류식 ,증류주 ,증류주를 ,증류하는 ,증류하는_감압식 ,증류하여 ,증류한 ,진득한 ,진한 ,질감을 ,집에서 ,짙은 ,짭조름한 ,짭짤한 ,차가운 ,차갑게 ,찹쌀과 ,첨가물 ,청량감 ,청포도 ,치즈 ,친구들과 ,크라테 ,탁주 ,탁주는 ,탁주의 ,탄산 ,탄산과 ,탄산이 ,텁텁한 ,투명한 ,튀는 ,특별한 ,특유의 ,특징이 ,편안하게 ,포도 ,포도로 ,포도를 ,포도의 ,풍미 ,풍미_짙은,풍미가 ,풍미가_짙은 ,풍미까지 ,풍미는 ,풍미를 ,풍미와 ,풍부하게 ,풍부한 ,해산물 ,향긋한 ,화이트 ,효모를 ,degree) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        data02 = tuple(result.values[0])

        try:
            self.cursor.execute(query)
            self.cursor.execute(query02, data02)
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
