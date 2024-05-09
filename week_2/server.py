from flask import Flask, make_response, request, jsonify
from fake_db import data

app = Flask(__name__)


@app.route("/no_content", methods=["GET"])
def no_content():
    return ({"message": "No content found"}, 204)


@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404


@app.route("/name_search", methods=["GET"])
def name_search():
    first_name = request.args.get("q")

    if not first_name:
        return {"message": "No first_name found in query parameters"}, 422

    try:
        for person in data:
            if person["first_name"].lower() == first_name.lower():
                return jsonify(person), 400
        return {"message": f"Person with name {first_name} not found"}, 404
    except Exception as e:
        return {"message": f"An error occurred: {e}"}, 500


@app.route("/count_users", methods=["GET"])
def count_users():
    return {"message": f"Total number of users is {len(data)}"}


@app.route("/person/<uuid:uuid>", methods=["GET"])
def find_person_by_id(uuid):
    id = str(uuid)

    try:
        for person in data:
            if person["id"] == id:
                return jsonify(person), 200
        return {"message": f"Person with id: {id} not found"}, 404
    except Exception as e:
        return {"message": f"An error occurred: {e}"}, 500


@app.route("/person/<uuid:uuid>", methods=["DELETE"])
def delete_user_by_id(uuid):
    id = str(uuid)

    try:
        for person in data:
            if person["id"] == id:
                data.remove(person)
                return {"message": f"Person with id: {id} deleted"}, 200
        return {"message": f"Person with id: {id} not found"}, 404
    except Exception as e:
        return {"message": f"An error occurred: {e}"}, 500


@app.route("/person", methods=["POST"])
def add_by_uuid():
    if not request.json:
        return {"message": "No input data provided"}, 422

    try:
        person = request.json
        data.append(person)
        return {"message": "Person added successfully"}, 201
    except Exception as e:
        return {"message": f"An error occurred: {e}"}, 500


@app.route("/exp", methods=["GET"])
def index_explicit():
    res = make_response({"message": "Hello, World!"})
    res.status_code = 200
    return res


@app.route("/", methods=["GET"])
def general():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
