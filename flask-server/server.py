#-*- coding:utf-8 -*-
import json
from flask import Flask, request, session, jsonify
from detail import detail_info, item_list, user_sign, buy, reviews
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from datetime import timedelta
# secret_key 노출을 피하기 위해 .env 파일 생성
from dotenv import load_dotenv
import os 

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

# load .env
load_dotenv()

# jwt
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config["JWT_ALGORITHM"] = os.environ.get('JWT_ALGORITHM')
## access 토큰 만료시간 - 설정 안하면 15분이 기본임
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}}, supports_credentials=True)




# 설문조사 결과
# {al_data : { al_id, al_name, category, price, degree, img_link, score} ,,,} 일걸..?
@app.route("/survey_list")
def survey_list():
    ans1 = request.args.get('ans1')
    ans2 = request.args.get('ans2')
    ans3 = request.args.get('ans3')
    ans4 = request.args.get('ans4')
    ans5 = request.args.get('ans5')

    lst = item_list()
    return lst.survey(ans1, ans2, ans3, ans4, ans5)



# 디테일페이지에서 사용하는 것
# token_rank는 리스트 형태
# al_data 내부
    # {al_data : { al_id, al_name, category, price, degree, img_link, score},
    #  token_rank : [token1, token2, ,,,]}
@app.route("/detail")
def detail():
    # 일반적인 술 detail 요청
    al_id = request.args.get('al_id')
    detail_data = detail_info(alid = al_id)

    return jsonify(detail_data.detail_page(page=1))

@app.route("/detail_user")
@jwt_required()
def detail_user():
    # 세션에 존재할 때! (jwt가 존재)
    claims = get_jwt();

    c_id = claims["c_id"]
    al_id = request.args.get('al_id')

    #사용자용 토큰 순서 리턴
    detail_data = detail_info(cid = c_id, alid = al_id)

    return jsonify(detail_data.detail_page(page=1))



# 디테일 페이지 하단 부분  :  리뷰 데이터
    # { # : {'u_name', 'al_name', 'review', 'score', 'datetime'}}
    # 날짜 순으로 정렬함 => 순서대로 출력하면 됨
@app.route("/readreviews")
def read_reviews():
    al_id = request.args.get('al_id')

    rev = reviews(al_id)
    return rev.get_reviews()




# detail 에서 사용
# 리뷰 남기기 버튼을 생성해야하면 1이, 아니면 0이 반환됨
@app.route('/review_button')
def review_button():
    # 로그인 했을 때와 안했을 때를 구분해야함.
    #######################################################################
    c_id = session["id"]
    al_id = request.args.get('al_id')

    review = buy(c_id)
    return jsonify(review.review_button(al_id))




# 구매버튼 누르면 buy_info 내용에 저장됨
# c_id, al_id 필요  
    # c_id는 session에서 가져오고, al_id는 get으로 던져줘,,
# insert 성공하면 return 1 else return 0
@app.route('/purchase', methods=["POST"])
@jwt_required()
def purchase():
    # 로그인 안됐으면 로그인하라는 메세지 발송
    ##################
    # 로그인 된 경우
    claims = get_jwt();

    c_id = claims["c_id"]
    al_id = request.json["al_id"]

    pur = buy(c_id)
    result = pur.add_purchase(al_id)

    if(result == 0):
        return jsonify({"msg": "구매에 실패했습니다."}), 400
    else:
        return jsonify({"msg" : "구매를 완료하였습니다."}), 201






# 리뷰 적는거 성공하면 return 1 else 0
@app.route('/write_review', methods=["POST"])
@jwt_required()
def write_review():
    claims = get_jwt()

    c_id = claims["c_id"]
    c_name = claims["user_name"]
    al_id = request.json['al_id']
    al_name = request.json['al_name']
    review = request.json['review']
    score = request.json['score']


    rev = buy(c_id)
    result = rev.write_review(c_name, al_id, al_name, review, score)

    if(result == 0):
        return jsonify({"msg": "리뷰 남기기에 실패하였습니다."}), 400
    else:
        return jsonify({"user_name" : c_name, "al_name" : al_name}), 201

# 디테일 페이지에서 사용
# 아이템과 비슷한 토큰 분산을 가진 상위 6개 아이템 반환
# 내부 구조
    # { # : {al_id, al_name, category, price, degree, img_link, score}, #:{}, ...}
@app.route('/simitems')
def simitems():
    al_id = request.args.get('al_id')

    i = item_list()
    return i.get_sim_6(al_id)




# 사용자별 아이템 15개 추천
# 내부 구조
    # { # : {al_id, al_name, category, price, degree, img_link, score}, #:{}, ...}
@app.route("/recomm")
def recomm():
    rec = item_list()
    return rec.best_15()


@app.route("/recomm_user")
@jwt_required()
def recomm_user():
    claims = get_jwt();

    c_id = claims["c_id"]

    rec = item_list(cid=c_id)
    return rec.get_top15()



# 주종 별 알콜 리스트
# columns : ['al_id', 'al_name', 'category', 'price', 'degree', 'img_link']
@app.route("/alcohol")
def alcohol_list():
    category = request.args.get('category')
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list()
    return item_lst.get_alcohols_json(category)



# 로그인 후 세션 넘기기
@app.route('/signin', methods=["POST"])
def signin():
    user_id = request.json['id']
    user_pw = request.json['pw']

    user = user_sign()
    result = user.sign_in(user_id, user_pw)

    # 존재하는 계정이 없는 경우 : 401 Unauthorized
    if(result == False):
        return jsonify({"msg": "Bad username or password"}), 401  
    
    # 계정이 존재 -> access_token 생성 : 200 OK
    # result에 유저 닉네임이 들어있음
    # c_id = result[0]
    # user_name = result[1]
    additional_claims = {"c_id": result[0], "user_name": result[1]}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)

    # access_token과 user_name을 클라이언트에 전달
    return jsonify({
        "access_token" : access_token
    }), 201

# 생성된 토큰 검증 후 토큰에 담긴 정보 해독하여 클라이언트로 보내주기
@app.route("/user_info", methods=["GET"])
@jwt_required()
def user_info():
    claims = get_jwt()
    return jsonify({
        "user_name" : claims["user_name"]
    })



# 회원가입 시 아이디 중복 확인  :  id 넘겨받음
    # 중복되면 return 0 else return 1
@app.route("/duplicate_id_check", methods=['POST'])
def duplicate_id_check():
    user_id = request.json['id']
    
    user = user_sign()
    result = user.duplicate_id_check(user_id)

    # 아이디 중복 : 409 Conflict
    if(result == 0):
        return jsonify({"msg": "이미 사용중인 아이디 입니다."}), 409
    
    # 중복 X : 200 OK
    return jsonify({"msg": "사용 가능한 아이디 입니다."})



# 회원가입 시 user_name 중복 확인  :  id 넘겨받음
    # 중복되면 return 0 else return 1
@app.route("/duplicate_name_check", methods=['POST'])
def duplicate_name_check():
    user_name = request.json['u_name']
    
    user = user_sign()
    result = user.duplicate_name_check(user_name)

    # 닉네임 중복 : 409 Conflict
    if(result == 0):
        return jsonify({"msg": "이미 사용중인 닉네임 입니다."}), 409
    
    # 중복 X : 200 OK
    return jsonify({"msg": "사용 가능한 닉네임 입니다."})




# 회원가입  :  u_id, u_pw, u_name 필요
    # 회원가입 성공하면 return 1 else 0
@app.route("/signup", methods=['POST'])
def sign_up():
    user_id = request.json['id']
    user_pw = request.json['pw']
    user_name = request.json['u_name']

    user = user_sign()
    result = user.sign_up(user_id, user_pw, user_name)
    
    if(result == 0):
        return jsonify({"msg": "회원가입에 실패했습니다."}), 400

    return jsonify({
        "id" : user_id,
        "name" : user_name,
        "msg" : "회원가입이 성공하였습니다."
    }), 201

# 리뷰 api

# mypage에서 사용
# 사용자가 구매한 아이템 리스트 출력
# columns  :  'c_id', 'al_id', 'al_name', 'date', 'review_O'
# 'review_o'의 값이 1이면, 리뷰 남기는 버튼 생성하면 됨
@app.route('/purchased_items')
@jwt_required()
def purchased_items():
    claims = get_jwt();

    user_id = claims["c_id"]

    items = buy(user_id)
    return items.purchase_items()




if __name__ == "__main__":
    app.run(debug=True) 