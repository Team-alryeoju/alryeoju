import pandas as pd
import numpy as np

# 개별 사용자-토큰 정보 가져오기  :  이후 sql로 대체
users_data = pd.read_csv('./db_csv/user_token.csv', encoding='cp949')
# 아이템 정보
items_data = pd.read_csv('./db_csv/id_token_img.csv', encoding='cp949')
# 술 기본 정보
sools_info = pd.read_csv('./db_csv/sool-detail.csv', encoding='cp949')
# 사용자별 아이템 순위
# raking[n]  :  n 번째 사용자의 알콜 추천 순위
rankings = pd.read_csv('./db_csv/ranking_new.csv')



class detail_info:
    def __init__(self, cid, alid):
        self.c_id = cid
        self.al_id = alid
        self.c_name = ''
        self.al_name = ''
        self.al_img = ''


    def search_al_id_token(self, al_id):
        # sql로 대체,,
        al_info = items_data.loc[items_data['id'] == al_id]
        self.al_name = al_info['alname']
        self.al_img = al_info['img'].to_list()[0]
        al_info.drop(columns=['alname','img'], inplace=True)
        return al_info

    def search_user_token(self, c_id):
        # sql로 대체,,
        user_info = users_data.loc[users_data['c_id'] == c_id]
        self.c_name = user_info['c_name']
        user_info.drop(columns=['c_name'], inplace=True)
        return user_info

    def get_token_rank(self):
        # 셋팅  :  사용자, 술 아이디 설정 및 해당 데이터 가져오기
        al_info = self.search_al_id_token(self.al_id)
        user_info = self.search_user_token(self.c_id)

        # 토큰 칼럼만 남김
        user_info.drop(columns = ['c_id'], inplace = True)  
        al_info.drop(columns=['id'], inplace = True)


        al_tokens = al_info.replace(0, np.NAN).T.dropna().index.to_list()
        user_token_score = user_info.replace(0, np.NaN).T.dropna()
        user_token_score.reset_index(inplace=True)
        token_seq = user_token_score[user_token_score['index'].isin(al_tokens)].sort_values(by = self.c_id, ascending=False)
        token_rank = token_seq['index'].values.tolist()
        return token_rank



####################################

class item_list:

    def __init__(self, cid):
        self.c_id = cid

    def get_top15_df(self):
        rankings_t = rankings.reset_index().drop(columns='index').T
        rankings_t.reset_index(inplace=True)

        rank_df = pd.DataFrame()
        # 1~15등 rank 칼럼 생성
        rank_df['rank'] = np.arange(1,16)
        # merge를 위해 인덱스 리셋
        rank_df.index = np.arange(1, 16)
        rank_df['al_name'] = rankings_t[self.c_id][1:16]
        rank_df = pd.merge(rank_df, items_data[['alname', 'id', 'img']], left_on='al_name', right_on='alname', how='inner').drop(columns='alname')
        rank_df['c_id'] = self.c_id

        # sool_info에서 category, degree, snack 칼럼 추가
        sool_info = sools_info[['id', 'category', 'degree', 'alname', 'snack']].copy()
        rank_df = pd.merge(rank_df, sool_info, on='id', how='inner').drop(columns='alname')
        rank_df = rank_df[['rank', 'id', 'al_name', 'category', 'degree', 'snack', 'c_id', 'img']]        
        
        return rank_df

    def get_top15_json(self):
        rank_df = self.get_top15_df()
        return rank_df.T.to_json(force_ascii=False)

    def get_alcohols_df(self):
        sool_info = sools_info[['id', 'category', 'degree', 'alname', 'snack']]
        item_data = items_data[['alname', 'id', 'img']] 
        items = pd.merge(sool_info, item_data, on='id', how='inner').drop(columns='alname_x').rename(columns={'alname_y':'al_name'})
        items['c_id'] = self.c_id
        items = items[['id', 'al_name', 'category', 'degree', 'snack', 'c_id', 'img']]
        return items

    def get_takju_json(self):
        sool = self.get_alcohols_df()
        takju = sool.loc[sool['category'] == '탁주']
        return takju.T.to_json(force_ascii=False)

    def get_yackju_json(self):
        sool = self.get_alcohols_df()
        takju = sool.loc[sool['category'] == '약주']
        return takju.T.to_json(force_ascii=False)
    
    def get_wine_json(self):
        sool = self.get_alcohols_df()
        takju = sool.loc[sool['category'] == '과실주']
        return takju.T.to_json(force_ascii=False)

    def get_soju_json(self):
        sool = self.get_alcohols_df()
        takju = sool.loc[sool['category'] == '일반증류주']
        return takju.T.to_json(force_ascii=False)
    
    def get_alcohol_random_json(self):
        sool = self.get_alcohols_df()
        sool = sool.sample(frac=1)
        return sool.T.to_json(force_ascii=False)
