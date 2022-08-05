from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'index'

    from app import db
    #db.init_app(app)

    from app import sub
    app.register_blueprint(sub.bp)

    return app