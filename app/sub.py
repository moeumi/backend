from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/sub')
def sub():
    return 'sub'
