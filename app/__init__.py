import os

from flask import Flask, current_app


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/')
    def index():
        return 'index'

    from app import db
    with app.app_context():
        db.init_app(app)

    from app import api
    app.register_blueprint(api.bp)

    from app import crawling
    app.register_blueprint(crawling.bp)
    #busan_lib_event()

    return app