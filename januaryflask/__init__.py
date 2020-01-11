import os
from firebase_admin import auth

from flask import Flask, request, jsonify
from . import db
connection = db.init_db()


def authorize(role):
    def wrapper(func):
        def authorize_and_call(*args, **kwargs):
            try:
                id_token = request.args.get('id_token')
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']
            except:
                return 'invalid id_token'
            try:
                doc_ref = connection.collection(
                    u'users').document(uid).get()
                print('doc_ref: {}'.format(doc_ref.to_dict()))
                if doc_ref.to_dict():
                    if role == doc_ref.to_dict()['permission_level']:
                        print('role requirement met')
                        return func(*args, **kwargs)
                    else:
                        return 'Unauthorized Access!'
                else:
                    'no user exists'
            except Exception as e:
                return "not authorized: {}".format(e)

        return authorize_and_call
    return wrapper


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import chat
    app.register_blueprint(chat.bp)
    from . import user
    app.register_blueprint(user.bp)
    @app.route('/testpost', methods=['POST'])
    def create():
        return db.create(connection, u'test', {
            u'first': u'a',
            u'last': u'lem',
            u'born': 1123
        })

    @app.route('/testauth')
    @authorize('admin')
    def create():
        return 'You are authed and this passed'
    return app
