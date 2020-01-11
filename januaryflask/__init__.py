import os

from flask import Flask, request, jsonify
from . import db
connection = db.init_db()


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
    return app
