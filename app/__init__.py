from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'index'

    from app import db
    #db.init_app(app)

    from app import api
    app.register_blueprint(api.bp)

    return app