from januaryflask import connection
import functools
from firebase_admin import exceptions
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
# from januaryflask.db import init_db

bp = Blueprint('user', __name__, url_prefix='/user')

# Get user by user id
@bp.route('/')
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
def update_user():

    data = request.get_json()

    return 'updated'
