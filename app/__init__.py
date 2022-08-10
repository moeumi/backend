import os

from flask import Flask



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
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

    from app import category
    from app import center
    from app import crawling
    from app import crawling_update

    #with app.app_context():
        #category.category()
        #center.center()
        #crawling.busan_lib_event()
        #crawling.busan_event()

    app.add_url_rule("/", endpoint="index")

    return app
