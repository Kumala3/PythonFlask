from flask import Flask, make_response, Request
from fake_db import data

app = Flask(__name__)

@app.route("/no_content", methods=["GET"])
def no_content():
    return ({"message": "No content found"}, 204)


@app.route("/exp", methods=["GET"])
def index_explicit():
    res = make_response({"message": "Hello, World!"})
    res.status_code = 200
    return res


@app.route("/", methods=["GET"])
def general(request: Request):
    first_name = request.query.get("first_name")
    return {"message": f"Hello, {first_name}"}


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
