from flask.blueprints import Blueprint
from flask import request, abort, jsonify
import json
from bson.objectid import ObjectId
from flask_mongoengine import ValidationError, DoesNotExist

from UserModel import User
__author__ = 'jacobgilsaa'

mod_user = Blueprint('mod_user', __name__, url_prefix='/api/user')


@mod_user.route('/get', methods=['GET'])
def get():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result={'message': 'Invalid token'}), 401
        user_profile = User.objects.get(userid=auth_token)
        if user_profile:
            print user_profile
            return jsonify(result={'profile': user_profile.get_profile()}), 200
        return jsonify(result={'message': 'Error in request'}), 400
    except KeyError:
        return jsonify(result={'message':'Error in request'}), 400

@mod_user.route('/login', methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        user_profile = User.objects.get(email=data['email'])
        if user_profile.verify_password(data['password']):
            return jsonify(result={'token': user_profile.generate_token()}), 200
        return jsonify(result={'message':'Email or password is incorrect. Please try again.'}), 401
    except KeyError:
        return jsonify(result={'message':'Error in request. Please try again.'}), 400
    except DoesNotExist:
        return jsonify(result={'message':'Email or password is incorrect. Please try again.'}), 401


@mod_user.route('/register', methods=['POST'])
def register():
    try:
        data = json.loads(request.data)
        if not User.objects(email=data['email']):
            user_profile = User(userid=str(ObjectId()), email=data['email'], firstname=data['firstname'], lastname=data['lastname'])
            user_profile.set_password(data['password'])
            user_profile.save()
            return jsonify(result={'token': user_profile.generate_token()}), 200
        return jsonify(result={'message':'Email already in use'}), 409
    except KeyError:
        return jsonify(result={'message':'Error in request. Please try again.'}), 400