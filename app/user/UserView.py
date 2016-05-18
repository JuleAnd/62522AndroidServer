from flask.blueprints import Blueprint
from flask import request, abort, jsonify
import json
from bson.objectid import ObjectId
from flask_mongoengine import ValidationError, DoesNotExist

from UserModel import User
__author__ = 'jacobgilsaa'

mod_user = Blueprint('mod_user', __name__, url_prefix='/api/user')


@mod_user.route('/get', methods=['GET'])
def test():
    print("get headers", request.headers)
    return jsonify(result='Got it'), 200


@mod_user.route('/login', methods=['POST'])
def login():
    try:
        print("post headers", request.headers)
        data = json.loads(request.data)
        user_profile = User.objects.get(email=data['email'])
        if user_profile.verify_password(data['password']):
            return jsonify(result={'profile': user_profile, 'token': user_profile.generate_token()}), 200
        return jsonify(result='Email or password is incorrect. Please try again.'), 401
    except KeyError:
        return jsonify(result='Error in request. Please try again.'), 400
    except DoesNotExist:
        return jsonify(result='Wrong username or password'), 401


@mod_user.route('/register', methods=['POST'])
def register():
    try:
        data = json.loads(request.data)
        if not User.objects(email=data['email']):
            user_profile = User(userid=str(ObjectId()), email=data['email'], firstname=data['firstname'], lastname=data['lastname'])
            user_profile.set_password(data['password'])
            user_profile.save()
            return jsonify(result={'profile': user_profile, 'token': user_profile.generate_token()}), 200
        return jsonify(result='Email already in use'), 409
    except KeyError:
        return jsonify(result='Error in request. Please try again.'), 400