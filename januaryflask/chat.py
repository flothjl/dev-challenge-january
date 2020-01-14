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
    data_keys = data.keys()
    data_keys = [item for item in data_keys if item in required_items]
    data_todb = {key: data[key] for key in data_keys}
    data['date_created'] = firestore.SERVER_TIMESTAMP
    try:
        doc_ref = connection.collection(u'chat').document()
        doc_ref.set(data, merge=True)
        return jsonify({"success": True})
    except Exception as e:
        return f"An Error Occured: {e}"
