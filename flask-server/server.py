from flask import Flask, render_template, request
from detail import detail_info, item_list

app = Flask(__name__)

# 디테일페이지에서 사용하는 것
# token_rank는 리스트 형태
# img_link는 str type
@app.route("/detail")
def detail():
    # c_id = request.args.get('id')
    # al_id = request.args.get('al_id')
    # detail_data = detail_info(c_id, al_id)
    detail_data = detail_info(1, 1124)
    token_rank = detail_data.get_token_rank()  # 주석금지
    img_link = detail_data.al_img
    return {'token_rank' : token_rank, 'img_link' : img_link}


# 사용자별 아이템 15개 추천
@app.rount("/recomm")
def recomm():
    # c_id = request.args.get('id')
    # recom_data = item_list(c_id)
    recom_data = item_list(3)
    # 칼럼 순서  :  rank, id, al_name, category, degree, snack, c_id, img
    return recom_data.get_top15_json()


# 전체(266개?) 행을 랜덤하게 섞어서 json으로 반환
@app.rount("/random")
def random_items():
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_alcohol_random_json()


# 탁주 json
@app.rout("/takju_list")
def takju_list():
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_takju_json()


# 약주 json
@app.rout("/yackju_list")
def yackkju_list():
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_yackju_json()


# 과실주 json
@app.rout("/wine_list")
def takju_list():
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_wine_json()


# 증류주 json
@app.rout("/soju_list")
def takju_list():
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_alcohol_random_json()


if __name__ == "__main__":
    app.run(debug=True) 