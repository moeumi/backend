import json

from flask import Blueprint, jsonify
from app.db import get_db
bp = Blueprint('main', __name__, url_prefix='/')

#페이지 fetch 필요
@bp.route('/contents')
def contents(): #all-contents
    db=get_db()
    results = db.execute(
        "SELECT * "
        "FROM test_contents"
    ).fetchall()

    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/district/<district_name>')
def district_contents(district_name):
    db=get_db()
    #page = request.args.get('page')
    results = db.execute(
        "SELECT *"
        "FROM contents INNER JOIN center"
        "ON contents.center_name=center.center_name and center.district_name = (?)",(district_name),
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/category/<category_name>')
def category_contents(category):
    db=get_db()
    results = db.executor(
        "SELECT *"
        "FROM contents"
        "WHERE contents.category = (?)", (category),
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/fontents/district/<district_name>/category/<category_name>')
def district_category_contents(district_name, category_name):
    db = get_db()
    results = db.executor(
        "SELECT *"
        "FROM contents INNER JOIN center"
        "ON contents.center_name = center.center_name and center.district_name=(?)",(district_name),
        "WHERE contents.category = (?)", (category_name),
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/center/<center_name>')
def center_contents(center_name):
    db = get_db()
    results = db.executor(
        "SELECT *"
        "FROM contents"
        "WHERE contents.center_name= (?)", (center_name),
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/id/<contents_id>')
def id_contents(contents_id):
    db = get_db()
    results = db.executor(
        "SELECT *"
        "FROM contents"
        "WHERE contents.contens_id=(?)", (contents_id),
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/logo')
def logo():
    db=get_db()
    results=db.executor(
        "SELECT *"
        "FROM logo"
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)