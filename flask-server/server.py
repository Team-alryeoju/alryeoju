#-*- coding:utf-8 -*-
import json
from flask import Flask, request, session, jsonify
from detail import detail_info, item_list, user_sign
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "key"
app.config["SECRET_KEY"] = "pass"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
# app.config.from_object(__name__)

CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}}, supports_credentials=True)
jwt = JWTManager(app)



# 디테일페이지에서 사용하는 것
# token_rank는 리스트 형태
# img_link는 str type
@app.route("/detail")
def detail():
    c_id = session["id"]
    al_id = request.args.get('al_id')
    detail_data = detail_info(c_id, al_id)
    token_rank = detail_data.get_token_rank()  # 주석금지
    img_link = detail_data.img_link
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
    user_id = json.loads(request.data)["id"]
    user_pw = json.loads(request.data)["pw"]

    user = user_sign()
    result = user.sign_in(user_id, user_pw)

    if(result != 'False'):
       session["id"] = result[0]
       session["c_name"] = result[1]
       access_token = create_access_token(identity=id)
       response = app.response_class(response=json.dumps({"access_token": access_token}),
                                  status=200,
                                  mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





# 회원가입 시 아이디 중복 확인  :  id 넘겨받음
    # 중복되면 return 0 else return 1
@app.route("/duplicate_id_check", methods=['POST'])
def duplicate_id_check():
    user_id = request.json['id']
    
    user = user_sign()
    return jsonify(user.duplicate_id_check(user_id))



# 회원가입 시 user_name 중복 확인  :  id 넘겨받음
    # 중복되면 return 0 else return 1
@app.route("/duplicate_name_check", methods=['POST'])
def duplicate_name_check():
    user_name = request.json['u_name']
    
    user = user_sign()
    return jsonify(user.duplicate_name_check(user_name))




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


if __name__ == "__main__":
    app.run(debug=True) 