from flask.blueprints import Blueprint
from flask import request, abort, jsonify
import json
from bson.objectid import ObjectId
from flask_mongoengine import ValidationError, DoesNotExist
from TaskModel import Task
from app.user.UserModel import User
__author__ = 'jacobgilsaa'

mod_task = Blueprint('mod_task', __name__, url_prefix='/api/task')


@mod_task.route('/get', methods=['GET'])
def get_tasks():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result="invalid token"), 401
        tasks = Task.objects(userid=auth_token)
        return jsonify(result=tasks), 200
    except KeyError:
        return jsonify(result="Error in request"), 400


@mod_task.route('/getById', methods=['GET'])
def get_task_by_id():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result="invalid token"), 401
        task = Task.objects.get(userid=auth_token, taskid=str(request.args['taskid']))
        if task:
            return jsonify(result=task), 200
        return jsonify(result="could not find task"), 404
    except KeyError:
        return jsonify(result="Error in request"), 400


@mod_task.route('/create', methods=['POST'])
def create_task():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result="invalid token"), 401
        task_data = json.loads(request.data)
        #Get the creator
        creator = User.objects.get(userid=auth_token)
        createdby = creator.firstname + ' ' + creator.lastname
        # Create the task
        new_task = Task(userid=auth_token, taskid=str(ObjectId()), createdby=createdby, title=task_data['title'], description=task_data['description'])
        new_task.save()
        return jsonify(result="Task sucessfully created"), 200
    except KeyError:
        return jsonify(result="Error in request"), 400


@mod_task.route('/edit', methods=['POST'])
def edit_task():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result="invalid token"), 401
        task_data = json.loads(request.data)
        task = Task.objects.get(userid=auth_token, taskid=task_data['taskid'])
        task.title = task_data['title']
        task.description = task_data['description']
        task.save()
        return jsonify(result=task), 200
    except KeyError:
        return jsonify(result="Error in request"), 400


@mod_task.route('/delete', methods=['DELETE'])
def delete_task():
    try:
        user_token = request.headers.get('Authorization')
        auth_token = User.verify_token(user_token)
        if auth_token == 401:
            return jsonify(result="invalid token"), 401
        # Create the task
        task = Task.objects.get(userid=auth_token, taskid=str(request.args['taskid']))
        task.delete()
        return jsonify(result="Task sucessfully deleted"), 200
    except Exception as ee:
        ee.message
        return jsonify(result="Error in request"), 400
