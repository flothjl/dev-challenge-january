from januaryflask import connection
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
# from januaryflask.db import init_db

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/createchat', methods=['POST'])
def create():
    data = request.get_json()
    try:
        doc_ref = connection.collection(u'test').document()
        doc_ref.set(data, merge=True)
        return jsonify({"success": True})
    except Exception as e:
        return f"An Error Occured: {e}"
