from januaryflask import connection
from januaryflask import authorize
from firebase_admin import firestore
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
# from januaryflask.db import init_db

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/initiate', methods=['POST'])
@authorize(0)
def initiate_chat(user_id):
    required_items = ['participants']
    data = request.get_json()
    for item in required_items:
        if item not in [key for key in data.keys()]:
            return 'missing required fields'
    data['created_by'] = user_id
    data['participants'].append(user_id)
    data_keys = data.keys()
    data_keys = [item for item in data_keys if item in required_items]
    data = {key: data[key] for key in data_keys}
    data['date_created'] = firestore.SERVER_TIMESTAMP
    try:
        doc_ref = connection.collection(u'chat').document()
        doc_ref.set(data, merge=True)
        return jsonify({"success": True})
    except Exception as e:
        return f"An Error Occured: {e}"


@bp.route('/message', methods=['POST', 'DELETE'])
@authorize(0)
def message(user_id):
    if request.method == 'POST':

        required_items = ['text', 'media', 'chat_id']

        data = request.get_json()

        print(data.keys())
        for item in required_items:
            if item not in [key for key in data.keys()]:
                return 'missing required fields'
        data_keys = data.keys()
        data_keys = [item for item in data_keys if item in required_items]
        data = {key: data[key] for key in data_keys}
        try:
            data['user_id'] = user_id
            data['date_created'] = firestore.SERVER_TIMESTAMP
            chat_ref = connection.collection(
                u'chat').document(data['chat_id'])
            if not chat_ref.get().to_dict():
                return 'chat does not exist'
            chat_participants = chat_ref.get().to_dict()
            try:
                message_ref = chat_ref.collection(u'messages').document()
                message_ref.set(data, merge=True)
                return jsonify({"success": True})
            except Exception as e:
                return f'failed to create messsage. Error Message: {e}'
        except Exception as e:
            return f'Post fail: {e}'
        return 'POST'
    elif request.method == 'DELETE':
        return 'DELETE'
