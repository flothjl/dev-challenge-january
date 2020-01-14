import os
from firebase_admin import auth
import uuid
from flask import Flask, request, jsonify
from . import db
connection = db.init_db()


def authorize(role):
    # decorator to restrict endpoints based on 'permission level' in user table
    # roles: 0 = basic, 100 = admin
    def wrapper(func):
        def authorize_and_call(*args, **kwargs):
            try:
                session_key = request.args.get('session_key')
                session_ref = connection.collection(u'session').document(session_key).get().to_dict()
                user_id = session_ref['user_id']
                permission_level = session_ref['permission_level']
            except:
                return 'invalid session_key'
            try:
                
                if role <= permission_level:
                    print('role requirement met')

                    return func(user_id, *args, **kwargs)
                else:
                    return 'Unauthorized Access!'

            except Exception as e:
                return "not authorized: {}".format(e)
        authorize_and_call.__name__ = func.__name__
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
    from . import users
    app.register_blueprint(users.bp)
    from . import forums
    app.register_blueprint(forums.bp)
    @app.route('/auth')
    def authenticate():
        try:
            id_token = request.args.get('id_token')
            decoded_token = auth.verify_id_token(id_token)      
            user_id = decoded_token['user_id']
            session_key = uuid.uuid4()
            print('session_key: {}'.format(str(session_key)))
            data = decoded_token
            try:
                data['permission_level'] = connection.collection(
                    u'users').document(user_id).get().to_dict()['permission_level']
            except:
                return 'unable to get permission level'
            try:
                doc_ref = connection.collection(u'session').document(str(session_key))
                doc_ref.set(data, merge=True)
                return jsonify({"session_key": str(session_key)})
            except Exception as e:
                return f"An Error Occured: {e}"
           
        except:
            return 'invalid accessToken'
    @app.route('/isauthed')
    @authorize(0)
    def create(uid):
        return jsonify({"authed": True})
    return app
