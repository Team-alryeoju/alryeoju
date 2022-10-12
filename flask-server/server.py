from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/users")
def users():
    data = {"users" : [{"id" : 1, "name" : "yerin"}, {"id" : 2, "name" : "dalkong"}]}
    users = data['users']

    params = request.args.get("name")

    return {"users" : [{"id" : 1, "name" : "yerin"}, {"id" : 2, "name" : "dalkong"}]}

if __name__ == "__main__":
    app.run(debug=True) 