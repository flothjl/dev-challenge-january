from januaryflask import connection
from januaryflask import authorize

import functools
from firebase_admin import exceptions
from firebase_admin import firestore
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

# from januaryflask.db import init_db

bp = Blueprint('user', __name__, url_prefix='/user')

# Get user by user id
@bp.route('/get')
def get_user():
    if request.args.get('userid'):
        doc_ref = connection.collection(
            u'users').document(request.args.get('userid'))

        try:
            doc = doc_ref.get()
            if doc.to_dict():
                return(u'Document data: {}'.format(doc.to_dict()))
            else:
                return ('no doc')
        except exceptions.NotFoundError:
            return(u'No such document!')
        return "user request initiated"
    else:
        return "no userid given"


@bp.route('/update', methods=['POST'])
@authorize(0)
def update_user(uid):
    update_items = ['first', 'last', 'username']
    data = request.get_json()
    data_keys = data.keys()
    data_keys = [item for item in data_keys if item in update_items]
    data_todb = {key: data[key] for key in data_keys}
    data_todb['date_updated'] = firestore.SERVER_TIMESTAMP
    try:
        doc_ref = connection.collection(u'users').document(uid)
        doc_ref.set(data_todb, merge=True)
        return jsonify({"success": True})
    except Exception as e:
        return f"An Error Occured: {e}"


@bp.route('/update_permissions', methods=['POST'])
@authorize(100)
def update_permissions():
    return 'permissions updated'
