#-*- coding:utf-8 -*-
import json
from flask import Flask, request, session, jsonify
from detail import detail_info, item_list, user_sign, buy
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta

app = Flask(__name__)

# jwt
app.config["JWT_SECRET_KEY"] = 'qwlkjduoqlwkejhf1298739184'
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)

CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}}, supports_credentials=True)


# 디테일페이지에서 사용하는 것
# token_rank는 리스트 형태
# img_link는 str type
# 하하하하하하하하하하하핳 아이템 이름을 안넘김 하하하하하하하하하핳
@app.route("/detail")
def detail():
    # 로그인했을 때의 리턴값
    c_id = session["id"]
    al_id = request.args.get('al_id')
    detail_data = detail_info(c_id, al_id)
    token_rank = detail_data.get_token_rank()  # 주석금지
    img_link = detail_data.img_link
    # 로그인 하지 않았을 때는 아이템이 가진 모든 토큰 뱉어내기
    #############################
    return jsonify({'token_rank' : token_rank, 'img_link' : img_link})



# 사용자별 아이템 15개 추천
@app.route("/recomm")
def recomm():
    c_id = request.args.get('id')
    recom_data = item_list(c_id)
    # 칼럼 순서  :  'al_name', 'al_id', 'img_link', 'category', 'degree'
    return recom_data.get_top15_json()



# 주종 별 알콜 리스트
@app.route("/alcohol")
def alcohol_list():
    category = request.args.get('category')
    # c_id를 요구해서 아무 값이나 넣으면 됨,,
    item_lst = item_list(-1)
    return item_lst.get_alcohols_json(category)



# 로그인 후 세션 넘기기
@app.route('/signin', methods=["POST"])
def signin():
    user_id = request.json['id']
    user_pw = request.json['pw']

    user = user_sign()
    result = user.sign_in(user_id, user_pw)

    # 존재하는 계정이 없는 경우 : 401 Unauthorized
    if(result == 'False'):
        return jsonify({"msg": "Bad username or password"}), 401  
    
    # 계정이 존재 -> access_token 생성 : 200 OK
    access_token = create_access_token(identity=user_id)
    # access_token에 user_name도 넣어야하는데;;
    #####################################
    return jsonify(access_token=access_token)




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

    # 이름 중복 : 409 Conflict
    if(result == 0):
        return jsonify({"msg": "이미 사용중인 이름 입니다."}), 409
    
    # 중복 X : 200 OK
    return jsonify({"msg": "사용 가능한 이름 입니다."})




# 회원가입  :  u_id, u_pw, u_name 필요
    # 회원가입 성공하면 return 1 else 0
@app.route("/signup", methods=['POST'])
def sign_up():
    user_id = request.json['id']
    user_pw = request.json['pw']
    user_name = request.json['u_name']

    user = user_sign()
    return jsonify(user.sign_up(user_id, user_pw, user_name))



@app.route('/logout')
def logout():
    session.pop('id', None)


# 리뷰 api

# mypage에서 사용
# 사용자가 구매한 아이템 리스트 출력
# columns  :  'c_id', 'al_id', 'al_name', 'date', 'review_O'
# 'review_o'의 값이 1이면, 리뷰 남기는 버튼 생성하면 됨
@app.route('/purchased_items', methods=['POST'])
def purchased_items():
    user_id = request.json['id']

    items = buy(user_id)
    return items.purchase_items()




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
@app.route('/purchase')
def purchase():
    # 로그인 안됐으면 로그인하라는 메세지 발송
    ##################
    # 로그인 된 경우
    c_id = session['id']
    al_id = request.args.get('al_id')

    pur = buy(c_id)
    return jsonify(pur.add_purchase(al_id))


# 리뷰 적는거 성공하면 return 1 else 0
@app.route('/write_review')
def write_review():
    c_id = session['id']
    al_id = request.args.get('al_id')
    score = request.args.get('score')

    rev = buy(c_id)
    return jsonify(rev.write_review(al_id, score))



if __name__ == "__main__":
    app.run(debug=True) 