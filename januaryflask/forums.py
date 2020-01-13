from januaryflask import connection
from januaryflask import authorize

import functools
from firebase_admin import exceptions
from firebase_admin import firestore
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

# from januaryflask.db import init_db

bp = Blueprint('forums', __name__, url_prefix='/forums')


@bp.route('/categories', methods=['GET'])  # get list of all categories
@authorize(0)
def get_categories(uid):
    try:
        doc_ref = connection.collection(u'categories').stream()
        categories_list = []
        for category in doc_ref:
            category_dict = category.to_dict()
            category_dict['_id'] = category.id
            category_dict['subcategories'] = []

            categories_list.append(category_dict)
            sub_docs = connection.collection(u'categories').document(
                category.id).collection(u'subcategories').stream()
            print('sub_docs: {}'.format(sub_docs))
            for subcat in sub_docs:
                print('for loop: {}'.format(subcat))
                subcat_dict = subcat.to_dict()
                subcat_dict['_id'] = subcat.id
                category_dict['subcategories'].append(subcat_dict)

        return jsonify(categories_list)
    except Exception as e:
        return "Exception: ", e
