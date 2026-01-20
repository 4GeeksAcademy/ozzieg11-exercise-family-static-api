"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200



@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "Debes enviar información en el body"}), 400
    if 'first_name' not in body:
        return jsonify ({'msg': "Debes enviar el Nombre"}), 400
    if 'age' not in body:
        return jsonify ({'msg': "Debes enviar la Edad"}), 400
    if 'lucky_numbers' not in body:
        return jsonify ({'msg': "Debes enviar los numeros de la suerte"}), 400
    new_member = {
        'first_name' : body ['first_name'],
        'age' : body ['age'],
        'lucky_numbers': body ['lucky_numbers']
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted = jackson_family.delete_member(id) 
    if deleted:
        return jsonify({"done": deleted}), 200
    else:
        return jsonify({"mensaje": f"Miembro con ID {id} no encontrado"}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)