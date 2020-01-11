from januaryflask import connection
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
# from januaryflask.db import init_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def get_user():
    if request.args.get('userid'):
        return "user request initiated"
    else:
        return "no userid given"
        # data = request.get_json()
        # try:
        #     doc_ref = connection.collection(u'test').document()
        #     doc_ref.set(data, merge=True)
        #     return jsonify({"success": True})
        # except Exception as e:
        #     return f"An Error Occured: {e}"
